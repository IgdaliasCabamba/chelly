from qtpy.QtWidgets import QFrame


class BaseCompletionWidget(QFrame):
    def __init__(self, parent):
        super().__init__(parent)


__all__ = ["BaseCompletionWidget"]
