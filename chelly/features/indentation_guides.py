from textwrap import indent
from qtpy.QtGui import QPainter, QColor, QFontMetrics, QPen, QPaintEvent
from qtpy.QtCore import Qt
from ..core import Feature, TextEngine, Character
from typing import List
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
        
        @property
        def active(self) -> bool:
            return self.__active

        def set_max_level(self, guide_level):
            self.__max_level = guide_level
            return self

        def set_active(self, active: bool):
            self.__active = active

    @property
    def line_width(self) -> int:
        if self.settings.line_width:
            return self.settings.line_width
        return 1

    @line_width.setter
    def line_width(self, value: float) -> None:
        self.settings.line_width = value

    def __init__(self, editor):
        super().__init__(editor)
        self.editor.on_painted.connect(self.paint_lines)

    def __configure_painter(self, painter: QPainter) -> None:
        pen = QPen(self.editor.style.theme.indentation_guide.color)
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidthF(self.line_width)
        painter.setPen(pen)

    def get_indentation_cords(self, char) -> List[Guide]:
        
        def _append_guide(_line_num:int, _indent_count:int) -> None:
            _guide = (IndentationGuides.Guide(_line_num)
                .set_max_level(_indent_count))
            if current_line == _line_num:
                _guide.set_active(True)
            indentations_cords.append(_guide)


        current_line = TextEngine(self.editor).current_line_nbr
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
                        _append_guide(line_num, indent_count)

            else:
                matches = self.TABS_PATTERN.finditer(text)
                for match in matches:
                    indent_count = match.end()
                    _append_guide(line_num, indent_count)

        return indentations_cords

    @property
    def indentation_guides_for_spaces(self) -> List[Guide]:
        return self.get_indentation_cords(Character.SPACE)

    @property
    def indentation_guides_for_tabs(self) -> List[Guide]:
        return self.get_indentation_cords(Character.TAB)

    def paint_lines(self, event:QPaintEvent) -> None:
        with QPainter(self.editor.viewport()) as painter:
            font_metrics = QFontMetrics(self.editor.font())
            self.font_width = self.editor.properties.tab_stop_distance
            self.font_height = font_metrics.height()

            self.__configure_painter(painter)

            if self.editor.properties.indent_with_tabs:
                for guide in self.indentation_guides_for_tabs:
                    
                    if guide.active:
                        ...
                        #pen = painter.pen()
                        #pen.setColor(Qt.GlobalColor.darkBlue)
                        #painter.setPen(pen)

                    for level in range(guide.max_level):
                        rect = TextEngine(self.editor).cursor_rect(guide.line, level, offset=0)
                        painter.drawLine(rect.topLeft(), rect.bottomLeft())

            else:
                for guide in self.indentation_guides_for_spaces:
                    
                    if guide.active:
                        ...

                    for level in range(guide.max_level):              
                        spaces_level = level * self.editor.properties.indent_size          
                        rect = TextEngine(self.editor).cursor_rect(guide.line, spaces_level, offset=0)
                        painter.drawLine(rect.topLeft(), rect.bottomLeft())