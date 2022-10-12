from ..core import TextEngine, Feature, FontEngine, Character
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
        TextEngine(self.editor).mark_whole_doc_dirty() # TODO
        self.editor.repaint()

    @property
    def position(self):
        return self._margin_pos

    @position.setter
    def position(self, value):
        self._margin_pos = value
        
    def __init__(self, editor):
        super().__init__(editor)
        
        self.__cached_cursor_position:tuple = None

        self._margin_pos = 80
        self._color = QtGui.QColor('#72c3f0')
        self._pen = QtGui.QPen(self._color)

        self.editor.on_painted.connect(self._paint_margin)
        self.editor.repaint()

    def _paint_margin(self, event:QtGui.QPaintEvent):
        current_cursor_position = TextEngine(self.editor).cursor_position

        if self.__cached_cursor_position == current_cursor_position:
            return None

        self.__cached_cursor_position = current_cursor_position

        offset = self.editor.contentOffset().x() + self.editor.document().documentMargin()
        x80 = FontEngine(self.editor.font()).real_horizontal_advance(
            Character.LARGEST.value,
            min_zero=True) * self._margin_pos
        x80 += offset
        
        with QtGui.QPainter(self.editor.viewport()) as painter:
            painter.setPen(self._pen)
            painter.drawLine(x80, 0, x80, EdgeLine.LINE_COVER_VIEW_SIZE)
    