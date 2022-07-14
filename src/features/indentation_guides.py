from PySide6.QtGui import QPainter, QColor, QFontMetrics
from ..core import Feature

class IndentationGuides(Feature):
    def __init__(self, editor):
        super().__init__(editor)

        self.editor.on_painted.connect(self.paint_lines)
    
    def paint_lines(self, event):
        with QPainter(self.editor.viewport()) as painter:
            font = self.editor.font()
            font_metrics = QFontMetrics(font)
            self.font_width = font_metrics.horizontalAdvance(' ') * 4.5
            self.font_height = font_metrics.height()

            longest_line = 20
            from_top = 0
            painter.setPen(QColor(0, 100, 100))
            for i in range(0, longest_line):
                the_x = self.font_width + (i * self.font_width)
                painter.drawLine(the_x, from_top, the_x,
                                 from_top + self.font_height)

