from PySide6.QtGui import QFont, QTextCursor, QColor, QPainter
from PySide6.QtCore import Qt, QSize, QRect
from ..core import Panel, FontEngine

class LineNumberMargin(Panel):
    """Line Number Widget for Editor based 
    on https://github.com/luchko/QCodeEditor/blob/master/QCodeEditor.py
    and https://doc.qt.io/qtforpython/examples/example_widgets__codeeditor.html
    """

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.scrollable = True
        self.number_font = QFont()
    
    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the left, we only need
        to compute the width
        """
        return QSize(self.line_number_area_width, 0)

    @property
    def line_number_area_width(self) -> int:
        digits = 1
        max_num = max(1, self.editor.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = (FontEngine(self.font()).real_horizontal_advance('9', True) * digits) + 2
        return space
                    
    def paintEvent(self, event):
        super().paintEvent(event)
        with QPainter(self) as painter:
            for top, block_number, block in self.editor.visible_blocks:
                number = str(block_number + 1)
                    
                if block_number == self.editor.textCursor().blockNumber():
                    self.number_font.setBold(True)
                    painter.setPen(QColor("#000000"))
                else:
                    self.number_font.setBold(False)
                    painter.setPen(QColor("#717171"))
            
                painter.setFont(self.number_font)
                width = self.width()
                height = self.fontMetrics().height()
                painter.drawText(0, top, width, height, Qt.AlignmentFlag.AlignRight, number)