from ..core import TextEngine, Feature
from qtpy import QtGui

class EdgeLine(Feature):
    """ Displays a right margin at column the specified position.
    """
    @property
    def color(self):
        """
        Gets/sets the color of the margin
        """
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._pen = QtGui.QPen(self._color)
        TextEngine(self.editor).mark_whole_doc_dirty()
        self.editor.repaint()

    @property
    def position(self):
        """
        Gets/sets the position of the margin
        """
        return self._margin_pos

    @position.setter
    def position(self, value):
        self._margin_pos = value
        
    def __init__(self, editor):
        super().__init__(editor)
        self._margin_pos = 79
        self._color = QtGui.QColor('red')
        self._pen = QtGui.QPen(self._color)

        self.editor.on_painted.connect(self._paint_margin)
        self.editor.repaint()

    def _paint_margin(self, event:QtGui.QPaintEvent):
        """ Paints the right margin after editor paint event. """
        #font = QtGui.QFont(self.editor.font_size + self.editor.zoom_level)

        metrics = QtGui.QFontMetricsF(self.editor.font())
        pos = self._margin_pos
        offset = self.editor.contentOffset().x() + \
            self.editor.document().documentMargin()
        x80 = round(metrics.horizontalAdvance(' ') * pos) + offset
        
        with QtGui.QPainter(self.editor.viewport()) as painter:
            painter.setPen(self._pen)
            painter.drawLine(x80, 0, x80, 2 ** 16)