import PySide6
from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import (QColor, QFont, QFontMetrics, QPainter, QTextBlock,
                           QTextCursor, QTextOption)
from PySide6.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout,
                               QPlainTextEdit, QScrollBar, QVBoxLayout)
from .code_editor import CodeEditor
from .scrollbar import SliderArea

from ..core import (FeaturesExceptions, LexerExceptions, Panel, Properties,
                    PropertiesExceptions, TextEngine)
from ..managers import FeaturesManager, LanguagesManager


class MiniMap(CodeEditor):
    def __init__(self, parent):
        super().__init__(parent)

        self.editor = parent.editor
        self._amount_of_blocks = TextEngine(self.editor).line_count
        self.current_scroll_value = self.editor.verticalScrollBar().value()

        self.setTextInteractionFlags(Qt.NoTextInteraction)

        self.slider = SliderArea(self)
        self.slider.show()

        self.setMouseTracking(True)
        self.setTabStopDistance(QFontMetrics(
            self.font()).horizontalAdvance(' ') * 2)

        self.zoomOut(8)
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.editor.document().contentsChange.connect(self.update_contents)
        self.editor.on_painted.connect(self.update_ui)

    def scroll_slide(self, y_point: int):
        self.slider.move(0, y_point)

    def update_ui(self):
        self._scroll_slide()

    def update_contents(self, pos, charsrem, charsadd):
        line_number = TextEngine(self.editor).current_line_nbr
        TextEngine(self).move_cursor_to_line(line_number)
        text = TextEngine(self.editor).text_at_line(line_number)

        if self._amount_of_blocks == TextEngine(self.editor).line_count:
            TextEngine(self).set_text_at_line(
                self.textCursor().blockNumber(), text)
            TextEngine(self).move_cursor_to_line(line_number)
        else:
            self.document().setPlainText(
                self.editor.document().toPlainText()
            )
            TextEngine(self).move_cursor_to_line(
                TextEngine(self.editor).current_line_nbr
            )

        self._amount_of_blocks = TextEngine(self.editor).line_count

    def _scroll_slide(self):
        num_editor_visible_lines = TextEngine(
            self.editor).visible_lines_from_line_count
        lines_on_editor_screen = TextEngine(self.editor).visible_lines

        if num_editor_visible_lines > lines_on_editor_screen:

            self._move_scroll(num_editor_visible_lines, lines_on_editor_screen)

            editor_line_nr = TextEngine(
                self.editor).line_number_from_position(0, 0)
            delta_y = TextEngine(self).point_y_from_line_number(editor_line_nr)

            # or:
            #   higher_pos = TextEngine(self.editor).position_from_point(0,0)
            #   delta_y = TextEngine(self).point_y_from_position(higher_pos)

            self.slider.move(0, delta_y)

        self.current_scroll_value = self.editor.verticalScrollBar().value()

    def _move_scroll(self, num_editor_visible_lines, lines_on_editor_screen):
        editor_first_visible_line = TextEngine(self.editor).first_visible_line
        editor_last_top_visible_line = num_editor_visible_lines - lines_on_editor_screen

        num_visible_lines = TextEngine(self).visible_lines_from_line_count
        lines_on_screen = TextEngine(self).visible_lines

        last_top_visible_line = num_visible_lines - lines_on_screen

        portion = editor_first_visible_line / editor_last_top_visible_line
        first_visible_line = round(last_top_visible_line * portion)

        self.verticalScrollBar().setValue(first_visible_line)

    def scroll_area(self, pos_parent, line_area) -> None:
        line = TextEngine(self).line_number_from_position(
            pos_parent.x(), pos_parent.y())
        self.editor.verticalScrollBar().setValue(line - line_area)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        TextEngine(self.editor).move_cursor_to_line(
            TextEngine(self).line_number_from_position(
                event.pos().x(), event.pos().y()
            )
        )

    def wheelEvent(self, event) -> None:
        super().wheelEvent(event)
        self.editor.wheelEvent(event)


class MiniChellyMap(Panel):
    
    class Properties:
        def __init__(self, minimap_container) -> None:
            self.__minimap_container = minimap_container
            self.__max_width:int = 140
            self.__min_width:int = 40
            self.__resizable:bool = True
            self.__drop_shadow = None
            self.default()
        
        def default(self):
            drop_shadow = QGraphicsDropShadowEffect(self.__minimap_container)
            drop_shadow.setColor(QColor("#111111"))
            drop_shadow.setXOffset(-3)
            drop_shadow.setYOffset(1)
            drop_shadow.setBlurRadius(6)
            self.shadow = drop_shadow
        
        @property
        def shadow(self) -> QGraphicsDropShadowEffect:
            return self.__drop_shadow
        
        @shadow.setter
        def shadow(self, new_shadow: QGraphicsDropShadowEffect) -> None:
            if isinstance(new_shadow, QGraphicsDropShadowEffect):
                self.__drop_shadow = new_shadow
                self.__minimap_container.setGraphicsEffect(self.__drop_shadow)
        
        @property
        def max_width(self) -> int:
            return self.__max_width
        
        @max_width.setter
        def max_width(self, width:int) -> None:
            if isinstance(width, int):
                self.__max_width = width
        
        @property
        def min_width(self) -> int:
            return self.__min_width
        
        @min_width.setter
        def min_width(self, width:int) -> None:
            if isinstance(width, int):
                self.__min_width = width
        
        @property
        def resizable(self) -> int:
            return self.__resizable
        
        @resizable.setter
        def resizable(self, value:bool) -> None:
            if isinstance(value, bool):
                self.__resizable = value


    def __init__(self, editor, properties= None):
        super().__init__(editor)
        self.__properties = MiniChellyMap.Properties(self)

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._minimap = MiniMap(self)

        self.box.addWidget(self._minimap)
        self.setLayout(self.box)
    
    @property
    def code_viewer(self) -> MiniMap:
        return self._minimap
    
    @property
    def properties(self) -> Properties:
        return self.__properties
    
    @properties.setter
    def properties(self, new_properties:Properties) -> None:
        if isinstance(new_properties, Properties):
            self.__properties = new_properties
    
    def activate_shadow(self):
        self.minimap.setGraphicsEffect(self.__drop_shadow)

    def disable_shadow(self):
        self.minimap.setGraphicsEffect(None)
    
    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the right, we only need
        to compute the width
        """
        return QSize(self.properties.max_width, self.fixed_size_hint)
