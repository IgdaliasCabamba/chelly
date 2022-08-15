"""
"""

from PySide6.QtGui import QPainter, QColor, QFontMetrics
from ..core import Feature, TextEngine
from dataclasses import dataclass
import re


class IndentationGuides(Feature):

    class Guide:
        def __init__(self, line):
            self.__line: int = line
            self.__level = 0

        @property
        def line(self):
            return self.__line
        
        @property
        def level(self):
            return self.__level

        def set(self, guide_level):
            self.__level = guide_level
            return self

    def __init__(self, editor):
        super().__init__(editor)

        self.editor.on_painted.connect(self.paint_lines)

    def paint_lines(self, event):
        indentations_cords = []
        visible_text = []

        for i in self.editor.visible_blocks:
            visible_text.append((i[2].text(), i[2].blockNumber()))
        
        for text, line_num in visible_text:
            if text.count(" "*4):
                splited_text = text.split(" "*4)
                
                indent_count = 0

                for item in splited_text:
                    if item=='':
                        indent_count += 1
                    else:
                        indentations_cords.append(
                            IndentationGuides.Guide(line_num).set(indent_count)
                        )
                        break
        
        with QPainter(self.editor.viewport()) as painter:
            
            font_metrics = QFontMetrics(self.editor.font())
            self.font_width = font_metrics.horizontalAdvance('W') * self.editor.properties.indent_size
            self.font_height = font_metrics.height()
            
            painter.setPen(QColor(0, 100, 100))

            for i in indentations_cords:
                for x in range(0, i.level-1):
                    the_x = self.font_width + (x * self.font_width)
                    painter.drawLine(the_x, TextEngine(self.editor).point_y_from_line_number(i.line), the_x,
                                    TextEngine(self.editor).point_y_from_line_number(i.line) + self.font_height)


