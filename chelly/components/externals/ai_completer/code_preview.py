from qtpy.QtWidgets import QFrame, QVBoxLayout, QTextEdit


class CodeFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.vbox = QVBoxLayout(self)
        self.setLayout(self.vbox)


__all__ = ["CodeFrame"]
