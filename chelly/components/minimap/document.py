from qtpy.QtCore import Qt
from qtpy.QtGui import QFontMetrics

#from ..api.chelly import ChellyEditor as CodeEditor
from ..code_editor import CodeEditor
from ...core import TextEngine, Character

class DocumentMap(CodeEditor):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor:CodeEditor = parent.editor
        self._amount_of_blocks = TextEngine(self.editor).line_count
        self.chelly_document = self.editor.chelly_document
        
        self.zoomOut(8)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setMouseTracking(True)
        self.setTabStopDistance(QFontMetrics(
            self.font()).horizontalAdvance(Character.LARGEST.value))
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
    def mouseMoveEvent(self, event) -> None:
        pass

    def mouseReleaseEvent(self, event) -> None:
        pass

    def wheelEvent(self, event) -> None:
        self.editor.wheelEvent(event)