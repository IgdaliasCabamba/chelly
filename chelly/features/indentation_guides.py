"""
"""
from typing import Any
from PySide6.QtGui import QPainter, QColor, QFontMetrics, QPen
from PySide6.QtCore import Qt
from ..core import Feature, TextEngine, Character
import re

class IndentationGuides(Feature):

    SPACES_PATTERN = re.compile(r'\A[^\S\n\t]+')
    TABS_PATTERN = re.compile(r'\A[\t]+')

    class Guide:
        def __init__(self, line):
            self.__line: int = line
            self.__active = False
            self.__max_level = 0

        @property
        def line(self):
            return self.__line
        
        @property
        def max_level(self):
            return self.__max_level

        def set_max_level(self, guide_level):
            self.__max_level = guide_level
            return self
        
        def set_active(self, active:bool):
            self.__active = active
    
    class Properties:
        def __init__(self, parent) -> None:
            self.__color = QColor(0, 100, 100)
            self.__active_color = [
                None, # acess control item
                self.__color
            ]
        
        @property
        def color(self) -> QColor:
            return self.__color
        
        @property
        def active_color(self) -> QColor:
            return self.__active_color[1]
        
        @color.setter
        def color(self, new_color:QColor) -> None:
            if isinstance(new_color, QColor):
                self.__color = new_color
                if self.__active_color[0] is None:
                    self.__active_color[1] = new_color
        
        @active_color.setter
        def active_color(self, new_color) -> None:
            self.__active_color[0] = Any
            self.__active_color[1] = new_color
        
    def __init__(self, editor):
        super().__init__(editor)
        self.__cached_cursor_pos = (-1,-1)
        self.__properties = IndentationGuides.Properties(self)
        self.editor.on_painted.connect(self.paint_lines)
    
    @property
    def properties(self) -> Properties:
        return self.__properties
    
    def __configure_painter(self, painter:QPainter) -> None:
        pen = QPen(self.properties.color)
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidthF(1)
        painter.setPen(pen)
    
    def get_indentation_cords(self, char) -> list:
        indentations_cords = []
        visible_text = []

        for top, block_number, block in self.editor.visible_blocks:
            visible_text.append(
                (block.text(), block_number)
            )
    
        for text, line_num in visible_text:
            
            if char == Character.SPACE:
                matches = self.SPACES_PATTERN.finditer(text)
                for match in matches:
                    match_end = match.end()
                    if match_end % self.editor.properties.indent_size == 0:
                        indent_count = match_end // self.editor.properties.indent_size
                        indentations_cords.append(
                            IndentationGuides.Guide(line_num)
                            .set_max_level(indent_count)
                        )
            else:
                matches = self.TABS_PATTERN.finditer(text)
                for match in matches:
                    indentations_cords.append(
                        IndentationGuides.Guide(line_num)
                        .set_max_level(match.end())
                    )
                        
        return indentations_cords
    
    def get_indentation_guides_for_spaces(self) -> list:
        #return self.get_indentation_cords(Character.SPACE.value * self.editor.properties.indent_size)
        return self.get_indentation_cords(Character.SPACE)
    
    def get_indentation_guides_for_tabs(self) -> list:
        return self.get_indentation_cords(Character.TAB)

    def paint_lines(self, event) -> None:
        if self.editor.horizontalScrollBar().value() > 0:
            return None
        
        current_cursor_pos = TextEngine(self.editor).cursor_position

        if self.__cached_cursor_pos == current_cursor_pos:
            return None
        else:
            self.__cached_cursor_pos = current_cursor_pos
            
        with QPainter(self.editor.viewport()) as painter:
            font_metrics = QFontMetrics(self.editor.font())
            self.font_width = self.editor.properties.tab_stop_distance
            #font_metrics.horizontalAdvance(Character.SPACE.value) * self.editor.properties.indent_size
            self.font_height = font_metrics.height()

            self.__configure_painter(painter)
            
            if self.editor.properties.indent_with_tabs:
                for guide in self.get_indentation_guides_for_tabs():
                    for level in range(-1, guide.max_level-1):
                        point_x = self.font_width + (level * self.font_width)

                        painter.drawLine(point_x, TextEngine(self.editor).point_y_from_line_number(guide.line), point_x,
                                    TextEngine(self.editor).point_y_from_line_number(guide.line) + self.font_height)
            else:
                for guide in self.get_indentation_guides_for_spaces():
                    for level in range(-1, guide.max_level-1):
                        point_x = self.font_width + (level * self.font_width)
                        point_x //= 2

                        painter.drawLine(point_x, TextEngine(self.editor).point_y_from_line_number(guide.line), point_x,
                                    TextEngine(self.editor).point_y_from_line_number(guide.line) + self.font_height)