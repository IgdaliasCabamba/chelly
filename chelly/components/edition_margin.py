from qtpy.QtGui import QFont, QPainter, QPen, QColor
from qtpy.QtCore import Qt, QSize
from ..core import Panel, FontEngine, TextEngine
import difflib

class EditionMargin(Panel):

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.scrollable = True
        self.number_font = QFont()
        self.__cached_lines_text = []
        self.differ = difflib.Differ()
    
    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the left, we only need
        to compute the width
        """
        return QSize(self.lines_area_width, 0)

    @property
    def lines_area_width(self) -> int:
        space = (FontEngine(self.editor.font()).real_horizontal_advance('|', True))
        return space
                    
    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        
        if self.editor.blockCount() <= 1:
            return None

        cached_lines_text_length = len(self.__cached_lines_text)
        if cached_lines_text_length >= 1000:
            return None
            
        first_v_block = self.editor.firstVisibleBlock().blockNumber()
        lines_text = []
        
        first_block = self.editor.document().firstBlock()
        
        if not self.__cached_lines_text:
            for text_block in list(TextEngine(self.editor).iterate_blocks_from(first_block)):
                lines_text.append(text_block.text())

            self.__cached_lines_text = lines_text.copy()
            return None
        
        else:
            for text_block in list(TextEngine(self.editor).iterate_blocks_from(first_block, cached_lines_text_length)):
                lines_text.append(text_block.text())
        
        pen = QPen()
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setWidth(8)
        point_x = 0
        height = self.editor.fontMetrics().height()
            
        if first_v_block <= cached_lines_text_length:
    
            diffs = list(self.differ.compare(self.__cached_lines_text, lines_text))
            
            with QPainter(self) as painter:

                for idx, diff in enumerate(diffs):
                    if diff.startswith(("-", "+", "?")):
                        top = TextEngine(self.editor).point_y_from_line_number(idx)

                        if diff.startswith("-"):
                            pen.setBrush(Qt.GlobalColor.darkRed)
                            painter.setPen(pen)
                            if self.settings.show_text_help:
                                painter.drawText(6, top+height//1.5, "!")

                        elif diff.startswith("+"):
                            pen.setBrush(Qt.GlobalColor.darkGreen)
                            painter.setPen(pen)
                            if self.settings.show_text_help:
                                painter.drawText(6, top+height//1.5, "+")

                        elif diff.startswith("?"):
                            pen.setBrush(Qt.GlobalColor.darkCyan)
                            painter.setPen(pen)
                            if self.settings.show_text_help:
                                painter.drawText(6, top+height//1.5, "?")
                        
                        painter.drawLine(point_x, TextEngine(self.editor).point_y_from_line_number(idx), point_x, TextEngine(self.editor).point_y_from_line_number(idx) + height)
        else:
            with QPainter(self) as painter:
                pen.setBrush(Qt.GlobalColor.darkGreen)
                painter.setPen(pen)
                if self.settings.show_text_help:
                    painter.drawText(6, top+height//1.5, "+")
                
                for _top, block_number, _block in self.editor.visible_blocks:
                    painter.drawLine(point_x, TextEngine(self.editor).point_y_from_line_number(block_number), point_x, TextEngine(self.editor).point_y_from_line_number(block_number) + height)