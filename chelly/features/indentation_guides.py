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
        self.__cached_cursor_pos = (-1, -1)
        self.editor.on_painted.connect(self.paint_lines)

    def __configure_painter(self, painter: QPainter) -> None:
        pen = QPen(self.editor.style.theme.indentation_guide.color)
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidthF(self.line_width)
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
                    indent_count = match.end()
                    indentations_cords.append(
                        IndentationGuides.Guide(line_num)
                        .set_max_level(indent_count)
                    )

        return indentations_cords

    def get_indentation_guides_for_spaces(self) -> list:
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
                        #point_x //= 2

                        painter.drawLine(point_x, TextEngine(self.editor).point_y_from_line_number(guide.line), point_x,
                                         TextEngine(self.editor).point_y_from_line_number(guide.line) + self.font_height)
