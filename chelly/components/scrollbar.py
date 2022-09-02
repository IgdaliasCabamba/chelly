from PySide6.QtWidgets import QScrollBar, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from ..core import Panel

class ScrollBar(QScrollBar):
    def __init__(self, editor, parent, orientation) -> None:
        super().__init__(parent)
        self.setOrientation(orientation)

class HorizontalScrollBar(Panel):
    def __init__(self, editor) -> None:
        super().__init__(editor)

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._scroll_bar = ScrollBar(self.editor, self, Qt.Horizontal)

        self.box.addWidget(self._scroll_bar)
        self.setLayout(self.box)
    
    @property
    def scrollbar(self):
        return self._scroll_bar
    
    def sizeHint(self) -> QSize:
        """
        Returns the panel size hint. (fixed with of 16px)
        """
        size_hint = QSize(w=14, h=14)
        size_hint.setWidth(14)
        size_hint.setHeight(14)
        return size_hint

class VerticalScrollBar(Panel):
    def __init__(self, editor) -> None:
        super().__init__(editor)

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._scroll_bar = ScrollBar(self.editor, self, Qt.Vertical)

        self.box.addWidget(self._scroll_bar)
        self.setLayout(self.box)
    
    @property
    def scrollbar(self):
        return self._scroll_bar
    
    def sizeHint(self) -> QSize:
        """
        Returns the panel size hint. (fixed with of 16px)
        """
        size_hint = QSize(w=14, h=14)
        size_hint.setWidth(14)
        size_hint.setHeight(14)
        return size_hint
        