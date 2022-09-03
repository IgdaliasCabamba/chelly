from PySide6.QtWidgets import QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor
from ..core import Panel

class BreadcrumbNav(Panel):
    def __init__(self, editor) -> None:
        super().__init__(editor)

        self.setStyleSheet("BreadcrumbNav QLabel{background:#2b2b2b}")
        self.scrollable = False
        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 2, 0, 0)

        self._breadcrumb = QLabel(self)
        self._breadcrumb.setText("<strong>Foo</strong> > <strong>bar</strong> > <strong>Hello</strong> > <strong>World</strong> > <strong>foobar</strong>  <strong>Foo</strong> > <strong>bar</strong> > <strong>Hello</strong> > <strong>World</strong> > <strong>foobar</strong>")

        self.box.addWidget(self._breadcrumb)
        self.setLayout(self.box)

        self.drop_shadow = QGraphicsDropShadowEffect(self)
        self.drop_shadow.setColor(QColor("#111111"))
        self.drop_shadow.setXOffset(-1)
        self.drop_shadow.setYOffset(2)
        self.drop_shadow.setBlurRadius(6)
        self.setGraphicsEffect(self.drop_shadow)

        self.editor.on_painted.connect(self.update_shadow)
        self.update_shadow()
    
    def update_shadow(self):
        if self.editor.verticalScrollBar().value() > 0:
            self.drop_shadow.setColor(QColor("#111111"))
        else:
            self.drop_shadow.setColor(QColor(Qt.GlobalColor.transparent))
        
    
    def sizeHint(self) -> QSize:
        """
        Returns the panel size hint. (fixed with of 16px)
        """
        size_hint = QSize(w=20, h=20)
        size_hint.setWidth(20)
        size_hint.setHeight(20)
        return size_hint