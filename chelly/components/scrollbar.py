from qtpy.QtWidgets import QScrollBar, QHBoxLayout, QVBoxLayout
from qtpy.QtCore import Qt, QSize
from ..core import Panel


class ScrollBar(QScrollBar):
    def __init__(self, editor, parent, orientation) -> None:
        super().__init__(parent)
        self.setOrientation(orientation)


class HorizontalScrollBar(Panel):
    def __init__(self, editor) -> None:
        super().__init__(editor)

        self.__is_moving = False

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._scroll_bar = ScrollBar(self.editor, self, Qt.Horizontal)

        self.box.addWidget(self._scroll_bar)
        self.setLayout(self.box)

        self.editor.on_painted.connect(self.update_values)
        self.editor.horizontalScrollBar().rangeChanged.connect(self.set_range)
        self._scroll_bar.sliderMoved.connect(self._start_scroll_editor)
        self._scroll_bar.sliderReleased.connect(self._stop_scroll_editor)
        self._scroll_bar.valueChanged.connect(self._set_value)

    def _set_value(self, value):
        self.editor.horizontalScrollBar().setValue(value)

    def _stop_scroll_editor(self):
        self.__is_moving = False

    def _start_scroll_editor(self):
        self.__is_moving = True

    def set_range(self, min, max):
        self._scroll_bar.setRange(min, max)

    def set_value(self, value):
        self._scroll_bar.setValue(value)

    def update_values(self):
        if not self.__is_moving:
            self.set_value(self.editor.horizontalScrollBar().value())
            self.set_range(0, self.editor.horizontalScrollBar().maximum())
            self._scroll_bar.setPageStep(self.editor.horizontalScrollBar().pageStep())

    @property
    def scrollbar(self):
        return self._scroll_bar

    def sizeHint(self) -> QSize:
        """
        Returns the panel size hint
        """
        size_hint = QSize(14, 14)
        size_hint.setWidth(14)
        size_hint.setHeight(14)
        return size_hint


class VerticalScrollBar(Panel):
    def __init__(self, editor) -> None:
        super().__init__(editor)

        self.__is_moving = False

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._scroll_bar = ScrollBar(self.editor, self, Qt.Vertical)

        self.box.addWidget(self._scroll_bar)
        self.setLayout(self.box)

        self.editor.on_painted.connect(self.update_values)
        self.editor.verticalScrollBar().rangeChanged.connect(self.set_range)
        self._scroll_bar.sliderMoved.connect(self._start_scroll_editor)
        self._scroll_bar.sliderReleased.connect(self._stop_scroll_editor)
        self._scroll_bar.valueChanged.connect(self._set_value)

    def _set_value(self, value):
        self.editor.verticalScrollBar().setValue(value)

    def _start_scroll_editor(self):
        self.__is_moving = True

    def _stop_scroll_editor(self):
        self.__is_moving = False

    def set_range(self, min, max):
        self._scroll_bar.setRange(min, max)

    def set_value(self, value):
        self._scroll_bar.setValue(value)

    def update_values(self):
        if not self.__is_moving:
            self.set_value(self.editor.verticalScrollBar().value())
            self.set_range(0, self.editor.verticalScrollBar().maximum())
            self._scroll_bar.setPageStep(self.editor.verticalScrollBar().pageStep())

    @property
    def scrollbar(self):
        return self._scroll_bar

    def sizeHint(self) -> QSize:
        """
        Returns the panel size hint
        """
        size_hint = QSize(14, 14)
        size_hint.setWidth(14)
        size_hint.setHeight(14)
        return size_hint


__all__ = ["HorizontalScrollBar", "ScrollBar", "VerticalScrollBar"]
