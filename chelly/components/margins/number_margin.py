from qtpy.QtGui import QFont, QTextCursor, QColor, QPainter
from qtpy.QtCore import Qt, QSize, QRect
from ...core import Panel, FontEngine
from ...internal import chelly_property
from typing import Any
from dataclasses import dataclass

class LineNumberMargin(Panel):
    """Line Number Widget for Editor based 
    on https://github.com/luchko/QCodeEditor/blob/master/QCodeEditor.py
    and https://doc.qt.io/qtforpython/examples/example_widgets__codeeditor.html
    """
    @dataclass(frozen=True)
    class Defaults:
        ...

    class Properties(Panel._Properties):
        def __init__(self, instance: Any) -> None:
            super().__init__(instance)
            self._background = QColor(Qt.GlobalColor.transparent)
            self._foreground = QColor(Qt.GlobalColor.darkGray)
            self._highlight = QColor(Qt.GlobalColor.lightGray)
        
        @chelly_property
        def foreground(self) -> QColor:
            return self._foreground

        @foreground.setter
        def foreground(self, new_color: QColor) -> None:
            self._foreground = new_color

        @chelly_property
        def background(self) -> QColor:
            return self._background

        @background.setter
        def background(self, new_color: QColor) -> None:
            self._background = new_color
        
        @chelly_property
        def highlight(self) -> QColor:
            return self._highlight

        @highlight.setter
        def highlight(self, new_color: QColor) -> None:
            self._highlight = new_color

    @property
    def properties(self) -> Properties:
        return self.__properties
    
    @properties.setter
    def properties(self, new_properties:Properties) -> Properties:
        if new_properties is LineNumberMargin.Properties:
            self.__properties = new_properties(self)

        elif isinstance(new_properties, LineNumberMargin.Properties):
            self.__properties = new_properties

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.__properties = LineNumberMargin.Properties(self)
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
                    painter.setPen(self.properties.highlight)
                else:
                    self.number_font.setBold(False)
                    painter.setPen(self.properties.foreground)
            
                painter.setFont(self.number_font)
                width = self.width()
                height = self.fontMetrics().height()
                painter.drawText(0, top, width, height, Qt.AlignmentFlag.AlignRight, number)