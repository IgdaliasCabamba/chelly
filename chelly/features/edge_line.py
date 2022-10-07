from ..core import TextEngine, Feature
from qtpy import QtGui

class EdgeLine(Feature):
    LINE_COVER_VIEW_SIZE = 2 ** 16

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._pen = QtGui.QPen(self._color)
        TextEngine(self.editor).mark_whole_doc_dirty()
        self.editor.repaint()

    @property
    def position(self):
        return self._margin_pos

    @position.setter
    def position(self, value):
        self._margin_pos = value
        
    def __init__(self, editor):
        super().__init__(editor)
        self._margin_pos = 80
        self._color = QtGui.QColor('#72c3f0')
        self._pen = QtGui.QPen(self._color)

        self.editor.on_painted.connect(self._paint_margin)
        self.editor.repaint()

    def _paint_margin(self, event:QtGui.QPaintEvent):
        pos = self._margin_pos
        offset = self.editor.contentOffset().x() + self.editor.document().documentMargin()
        x80 = TextEngine(self.editor).cursor_rect(0, pos, offset=offset)
        
        with QtGui.QPainter(self.editor.viewport()) as painter:
            painter.setPen(self._pen)
            painter.drawLine(x80.left(), 0, x80.right(), EdgeLine.LINE_COVER_VIEW_SIZE)
    