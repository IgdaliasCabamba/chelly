from typing import Any
from dataclasses import dataclass
from qtpy.QtGui import QFont, QPainter, QPen, QColor
from qtpy.QtCore import Qt, QSize
from ...core import Panel, FontEngine, TextEngine, ChellyCache
import difflib

class EditionMargin(Panel):
    
    @dataclass(frozen=True)
    class Defaults:
        SHOW_TEXT_HELP = False
        MAX_LINES_COUNT = 1000
        
    class Properties(Panel._Properties):

        def __init__(self, panel:Panel):
            super().__init__(panel)
            
            self._unknow = Qt.GlobalColor.darkCyan
            self._added = Qt.GlobalColor.darkGreen
            self._removed = Qt.GlobalColor.darkRed

            self.__show_text_help = EditionMargin.Defaults.SHOW_TEXT_HELP
            self.__max_lines_count = EditionMargin.Defaults.MAX_LINES_COUNT
        
        @property
        def show_text_help(self) -> bool:
            return self.__show_text_help
        
        @show_text_help.setter
        def show_text_help(self, show:bool) -> None:
            self.__show_text_help = show
        
        @property
        def max_lines_count(self) -> int:
            return self.__max_lines_count
        
        @max_lines_count.setter
        def max_lines_count(self, limit:int) -> None:
            self.__max_lines_count = limit
        
        @property
        def unknow(self) -> QColor:
            return self._unknow
        
        @unknow.setter
        def unknow(self, color:QColor) -> None:
            self._unknow = color
        
        @property
        def added(self) -> QColor:
            return self._added
        
        @added.setter
        def added(self, color:QColor) -> None:
            self._added = color
        
        @property
        def removed(self) -> QColor:
            return self._removed
        
        @removed.setter
        def removed(self, color:QColor) -> None:
            self._removed = color

    @property
    def properties(self) -> Properties:
        return self.__properties
    
    @properties.setter
    def properties(self, new_properties:Properties) -> Properties:
        if new_properties is EditionMargin.Properties:
            self.__properties = new_properties(self)

        elif isinstance(new_properties, EditionMargin.Properties):
            self.__properties = new_properties
        

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.scrollable = True
        self.number_font = QFont()
        self.__current_diffs = []
        self.__cached_lines_text = []
        self.__cached_cursor_position = ChellyCache(None, None, lambda: TextEngine(self.editor).cursor_position)
        self.differ = difflib.Differ()
        self.__properties = EditionMargin.Properties(self)
    
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
        if cached_lines_text_length >= self.properties.max_lines_count:
            return None
            
        first_v_block = self.editor.firstVisibleBlock().blockNumber()
        lines_text = []
        
        first_block = self.editor.document().firstBlock()
        
        if not self.__cached_lines_text:
            if self.editor.blockCount() > self.properties.max_lines_count:
                return None
                
            for text_block in list(TextEngine(self.editor).iterate_blocks_from(first_block)):
                lines_text.append(text_block.text())

            self.__cached_lines_text = lines_text.copy()
            return None
        
        else:
            for text_block in list(TextEngine(self.editor).iterate_blocks_from(first_block, cached_lines_text_length)):
                lines_text.append(text_block.text())
    
        if self.__cached_cursor_position.changed:
            diffs = list(self.differ.compare(self.__cached_lines_text, lines_text))
        else:
            diffs = self.__current_diffs
        
        pen = QPen()
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setWidth(8)
        point_x = 0
        height = self.editor.fontMetrics().height()
            
        if first_v_block <= cached_lines_text_length:
            
            self.__current_diffs = diffs
            
            with QPainter(self) as painter:

                for idx, diff in enumerate(self.__current_diffs):
                    if diff.startswith(("-", "+", "?")):
                        top = TextEngine(self.editor).point_y_from_line_number(idx)

                        if diff.startswith("-"):
                            pen.setBrush(self.properties.removed)
                            painter.setPen(pen)
                            if self.properties.show_text_help:
                                painter.drawText(6, top+height//1.5, "!")

                        elif diff.startswith("+"):
                            pen.setBrush(self.properties.added)
                            painter.setPen(pen)
                            if self.properties.show_text_help:
                                painter.drawText(6, top+height//1.5, "+")

                        elif diff.startswith("?"):
                            pen.setBrush(self.properties.unknow)
                            painter.setPen(pen)
                            if self.properties.show_text_help:
                                painter.drawText(6, top+height//1.5, "?")
                        
                        painter.drawLine(point_x, TextEngine(self.editor).point_y_from_line_number(idx), point_x, TextEngine(self.editor).point_y_from_line_number(idx) + height)
        else:
            with QPainter(self) as painter:
                pen.setBrush(Qt.GlobalColor.darkMagenta)
                painter.setPen(pen)
                if self.properties.show_text_help:
                    painter.drawText(6, top+height//1.5, "+")
                
                for _top, block_number, _block in self.editor.visible_blocks:
                    painter.drawLine(point_x, TextEngine(self.editor).point_y_from_line_number(block_number), point_x, TextEngine(self.editor).point_y_from_line_number(block_number) + height)