from textwrap import indent
from typing_extensions import Self
from qtpy.QtGui import QPainter, QColor, QFontMetrics, QPen, QPaintEvent
from qtpy.QtCore import Qt
from ..core import Feature, TextEngine, Character
from typing import List
from dataclasses import dataclass
import re

class IndentationGuides(Feature):

    SPACES_PATTERN = re.compile(r'\A[^\S\n\t]+')
    TABS_PATTERN = re.compile(r'\A[\t]+')

    class Guide:
        def __init__(self, line):
            self.__line: int = line
            self.__active_level = None
            self.__max_level = 0

        @property
        def line(self):
            return self.__line

        @property
        def max_level(self):
            return self.__max_level
        
        @property
        def active_level(self) -> int:
            return self.__active_level

        def set_max_level(self, guide_level) -> Self:
            self.__max_level = guide_level
            return self

        def set_active_level(self, level: int) -> Self:
            self.__active_level = level
            return self

    @dataclass(frozen=True)
    class Defaults:
        LINE_WIDTH = 1

    class Properties(Feature._Properties):
        def __init__(self, feature:Feature) -> None:
            super().__init__(feature)
            self.__line_width = IndentationGuides.Defaults.LINE_WIDTH

        @property
        def line_width(self) -> float:
            return self.__line_width

        @line_width.setter
        def line_width(self, value: float) -> None:
            self.__line_width = value
    
    @property
    def properties(self) -> Properties:
        return self.__properties
    
    @properties.setter
    def properties(self, new_properties:Properties) -> Properties:
        if new_properties is IndentationGuides.Properties:
            self.__properties = new_properties(self)

        elif isinstance(new_properties, IndentationGuides.Properties):
            self.__properties = new_properties

    def __init__(self, editor):
        super().__init__(editor)
        self.__properties = IndentationGuides.Properties(self)
        self.editor.on_painted.connect(self._paint_lines)

    def __configure_painter(self, painter: QPainter) -> None:
        pen = QPen(self.editor.style.theme.indentation_guide.color)
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidthF(self.properties.line_width)
        painter.setPen(pen)


    def get_indentation_cords(self, char) -> List[Guide]:
        
        def _append_guide(_line_num:int, _indent_count:int, active_level:int=None) -> None:
            _guide:IndentationGuides.Guide = (IndentationGuides.Guide(_line_num)
                .set_max_level(_indent_count)
                .set_active_level(active_level))
            indentations_cords.append(_guide)


        current_line = TextEngine(self.editor).current_line_nbr
        indentations_cords = []
        active_level = None
        
        for _, line_num, block in self.editor.visible_blocks:
            text = block.text()

            if char == Character.SPACE:
                matches = self.SPACES_PATTERN.finditer(text)
                for match in matches:
                    match_end = match.end()
                    if match_end % self.editor.properties.indent_size == 0:
                        indent_count = match_end // self.editor.properties.indent_size
                    
                        if active_level is None and current_line == line_num:
                            active_level = match.end()-1
                    
                        _append_guide(line_num, indent_count, active_level)

            else:
                matches = self.TABS_PATTERN.finditer(text)
                for match in matches:
                    indent_count = match.end()
                    
                    if active_level is None and current_line == line_num:
                        active_level = match.end()-1
                    
                    _append_guide(line_num, indent_count, active_level)
                    

        return indentations_cords

    @property
    def indentation_guides_for_spaces(self) -> List[Guide]:
        return self.get_indentation_cords(Character.SPACE)

    @property
    def indentation_guides_for_tabs(self) -> List[Guide]:
        return self.get_indentation_cords(Character.TAB)

    def _paint_lines(self, event:QPaintEvent) -> None:
        with QPainter(self.editor.viewport()) as painter:
            font_metrics = QFontMetrics(self.editor.font())
            self.font_width = self.editor.properties.tab_stop_distance
            self.font_height = font_metrics.height()

            self.__configure_painter(painter)
            pen = painter.pen()
            normal_pen = painter.pen()
            

            if self.editor.properties.indent_with_tabs:
                for guide in self.indentation_guides_for_tabs:

                    for level in range(guide.max_level):
                        
                        if guide.active_level == level:
                            pen.setColor(Qt.GlobalColor.darkBlue)
                            painter.setPen(pen)
                        else:
                            painter.setPen(normal_pen)

                        rect = TextEngine(self.editor).cursor_rect(guide.line, level, offset=0)
                        painter.drawLine(rect.topLeft(), rect.bottomLeft())

            else:
                for guide in self.indentation_guides_for_spaces:

                    for level in range(guide.max_level):
                        
                        if guide.active_level == level:
                            pen.setColor(Qt.GlobalColor.darkBlue)
                            painter.setPen(pen)
                        else:
                            painter.setPen(normal_pen)

                        spaces_level = level * self.editor.properties.indent_size          
                        rect = TextEngine(self.editor).cursor_rect(guide.line, spaces_level, offset=0)
                        painter.drawLine(rect.topLeft(), rect.bottomLeft())