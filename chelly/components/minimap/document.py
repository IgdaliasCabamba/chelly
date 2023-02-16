from qtpy.QtCore import Qt
from qtpy.QtGui import QFontMetrics

# from ..api.chelly import ChellyEditor as CodeEditor
from ..code_editor import CodeEditor
from ...core import TextEngine, Character


class DocumentMap(CodeEditor):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor: CodeEditor = parent.editor
        self.update_document()
        self.editor.on_chelly_document_changed.connect(self.update_document)

        self.zoomOut(8)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setMouseTracking(True)
        self.setTabStopDistance(
            QFontMetrics(self.font()).horizontalAdvance(Character.LARGEST.value)
        )
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def update_document(self):
        self.chelly_document = self.editor.chelly_document

    def mouseMoveEvent(self, event) -> None:
        return None

    def mouseReleaseEvent(self, event) -> None:
        return None

    def wheelEvent(self, event) -> None:
        return self.editor.wheelEvent(event)


__all__ = ["DocumentMap"]
