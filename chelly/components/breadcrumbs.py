from PySide6.QtWidgets import QLabel, QHBoxLayout
from PySide6.QtCore import QSize
from ..core import Panel, FontEngine, DelayJobRunner, TextEngine, TextDecoration

class BreadcrumbNav(Panel):
    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.setStyleSheet("background:#2b2b2b")
        self.scrollable = False
        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(16, 2, 0, 0)

        self._breadcrumb = QLabel(self)
        self._breadcrumb.setText("<strong>Foo</strong> > <strong>bar</strong> > <strong>Hello</strong> > <strong>World</strong> > <strong>foobar</strong>")

        self.box.addWidget(self._breadcrumb)
        self.setLayout(self.box)
    
    def sizeHint(self) -> QSize:
        """
        Returns the panel size hint. (fixed with of 16px)
        """
        size_hint = QSize(w=0, h=16)
        size_hint.setWidth(16)
        size_hint.setHeight(16)
        return size_hint