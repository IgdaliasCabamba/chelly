from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from .breadcrumbs import Breadcrumb

class ChellyEditor(QTextEdit):
    pass

class CodeEditor(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.build()
    
    def build(self):
        self.container = QVBoxLayout(self)
        self.setLayout(self.container)
        self.container.setContentsMargins(0,0,0,0)

        self.breadcrumb = Breadcrumb(self)
        self.chelly_editor = ChellyEditor(self)

        self.container.addWidget(self.breadcrumb)
        self.container.addWidget(self.chelly_editor)
