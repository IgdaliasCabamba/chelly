from typing import Union
from qtpy.QtGui import QBrush, QIcon, QColor, QPainter, QTextDocument, QFontMetricsF
from qtpy.QtCore import Qt, QSize, QRect, QObject, Signal, QPoint
from qtpy.QtWidgets import QToolTip, QStyle
from ...internal import chelly_property
from ...core import Panel, FontEngine, DelayJobRunner, TextEngine, TextDecoration


class MarkerObject(QObject):
    """
    A marker is an icon draw on a marker panel at a specific line position and
    with a possible tooltip.
    """

    @property
    def position(self):
        """
        Gets the marker position (line number)
        :type: int
        """
        try:
            return self.block.blockNumber()
        except AttributeError:
            return self._position  # not added yet

    @property
    def icon(self):
        """
        Gets the icon file name. Read-only.
        """
        if isinstance(self._icon, str):
            if QIcon.hasThemeIcon(self._icon):
                return QIcon.fromTheme(self._icon)
            else:
                return QIcon(self._icon)
        elif isinstance(self._icon, tuple):
            return QIcon.fromTheme(self._icon[0], QIcon(self._icon[1]))
        elif isinstance(self._icon, QIcon):
            return self._icon
        return QIcon()

    @property
    def description(self):
        """Gets the marker description."""
        return self._description

    def __init__(self, position, icon="", description="", parent=None):
        """
        :param position: The marker position/line number.
        :type position: int
        :param icon: The icon to display
        :type icon: QIcon
        :param parent: The optional parent object.
        :type parent: QObject or None
        """
        super().__init__(parent)
        #: The position of the marker (line number)
        self._position = position
        self._icon = icon
        self._description = description


class MarkerMargin(Panel):
    class Properties(Panel._Properties):
        def __init__(self, panel: Panel):
            super().__init__(panel)
            self._background = QColor("#FFC8C8")

        @chelly_property
        def background(self) -> QColor:
            """
            Marker background color in editor. Use None if no text decoration
            should be used.
            """
            return self._background

        @background.setter
        def background(self, value):
            self._background = value

    @property
    def properties(self) -> Properties:
        return self.__properties

    @properties.setter
    def properties(self, new_properties: Properties) -> Properties:
        if new_properties is MarkerMargin.Properties:
            self.__properties = new_properties(self)

        elif isinstance(new_properties, MarkerMargin.Properties):
            self.__properties = new_properties

    on_add_marker = Signal(int)

    on_edit_marker = Signal(int)

    on_remove_marker = Signal(int)

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self._markers = []
        self._icons = {}
        self._previous_line = -1
        self.scrollable = True
        self._job_runner = DelayJobRunner(delay=100)
        self.setMouseTracking(True)
        self._to_remove = []
        self.__properties = MarkerMargin.Properties(self)

    @property
    def markers(self) -> list:
        """
        Gets all markers.
        """
        return self._markers

    def add_marker(self, marker: MarkerObject):
        """
        Adds the marker to the panel.
        :param marker: Marker to add
        :type marker: pyqode.core.modes.Marker
        """
        self._markers.append(marker)
        block = TextEngine(self.editor).block_from_line_number(marker._position)

        marker.block = block

        # block_decoration = (
        #    TextDecoration(block)
        #    .set_full_width()
        #    .set_background(QBrush(self._background))
        # )
        # marker.decoration = block_decoration
        # self.editor.decorations.append(block_decoration)
        self.repaint()

    def __rem_marker(self, marker: MarkerObject):
        self._markers.remove(marker)
        self._to_remove.append(marker)

    def remove_marker(self, markers: Union[list, MarkerObject]):
        """
        Removes a marker from the panel
        :param marker: Marker to remove
        :type marker: Union[list, Marker]
        """
        if isinstance(markers, list):
            for marker in markers:
                self.__rem_marker(marker)

        elif isinstance(markers, MarkerObject):
            self.__rem_marker(markers)

        # if hasattr(markers, 'decoration'):
        # self.editor.decorations.remove(markers.decoration)
        self.repaint()

    def clear_markers(self):
        """Clears the markers list"""
        while len(self._markers):
            self.remove_marker(self._markers[0])

    def marker_for_line(self, line: int) -> list:
        """
        Returns the marker that is displayed at the specified line number if
        any.
        :param line: The marker line.
        :return: list of Markers for given line
        :rtype: list
        """
        markers = []
        for marker in self._markers:
            if line == marker.position:
                markers.append(marker)
        return markers

    def sizeHint(self) -> QSize:
        """
        Returns the panel size hint. (fixed with of 16px)
        """
        metrics = QFontMetricsF(self.editor.font())
        size_hint = QSize()
        size_hint.setWidth(16)
        size_hint.setHeight(int(metrics.height()))
        return size_hint

    def paintEvent(self, event):
        super().paintEvent(event)
        with QPainter(self) as painter:
            for top, block_nbr, block in self.editor.visible_blocks:
                for marker in self._markers:
                    if marker.block == block and marker.icon:
                        rect = QRect()
                        rect.setX(0)
                        rect.setY(top)
                        rect.setWidth(self.sizeHint().width())
                        rect.setHeight(self.sizeHint().height())
                        marker.icon.paint(painter, rect)

    def mousePressEvent(self, event):
        # Handle mouse press:
        # - emit add marker signal if there were no marker under the mouse
        #   cursor
        # - emit remove marker signal if there were one or more markers under
        #   the mouse cursor.
        line = TextEngine(self.editor).line_number_from_position(event.pos().y())
        if self.marker_for_line(line):
            if event.button() == Qt.LeftButton:
                self.on_remove_marker.emit(line)
            else:
                self.on_edit_marker.emit(line)
        else:
            self.on_add_marker.emit(line)

    def mouseMoveEvent(self, event):
        # Requests a tooltip if the cursor is currently over a marker.
        line = TextEngine(self.editor).line_number_from_position(event.pos().y())
        markers = self.marker_for_line(line)
        text = "\n".join(
            [marker.description for marker in markers if marker.description]
        )
        if len(markers):
            if self._previous_line != line:
                top = TextEngine(self.editor).point_y_from_line_number(
                    markers[0].position
                )
                if top:
                    self._job_runner.request_job(self._display_tooltip, text, top)
        else:
            self._job_runner.cancel_requests()
        self._previous_line = line

    def leaveEvent(self, *args, **kwargs):
        """
        Hide tooltip when leaving the panel region.
        """
        QToolTip.hideText()
        self._previous_line = -1

    def _display_tooltip(self, tooltip, top):
        """
        Display tooltip at the specified top position.
        """
        QToolTip.showText(
            self.mapToGlobal(QPoint(self.sizeHint().width(), top)), tooltip, self
        )


__all__ = ["MarkerMargin", "MarkerObject"]
