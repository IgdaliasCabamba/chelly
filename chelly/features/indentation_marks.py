from textwrap import indent
from qtpy.QtGui import QPainter, QColor, QFontMetrics, QPen, QPaintEvent, QBrush, QTextCursor
from qtpy.QtCore import Qt, QRect
from ..core import Feature, TextEngine, Character
from typing import List
import re

class IndentationMarks(Feature):

    SPACES_PATTERN = re.compile(r'\A[^\S\n\t]+')
    TABS_PATTERN = re.compile(r'\A[\t]+')

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
        self.editor.on_painted.connect(self.paint_indentation)

    def _chooseVisibleWhitespace(self, text):
        result = [False for _ in range(len(text))]
        lastNonSpaceColumn = len(text.rstrip()) - 1

        for column, char in enumerate(text[:lastNonSpaceColumn]):
            if char.isspace() and \
                (char == '\t' or \
                column == 0 or \
                text[column - 1].isspace() or \
                ((column + 1) < lastNonSpaceColumn and \
                    text[column + 1].isspace())):
                result[column] = True
        
        return result
    
    def paint_indentation(self, event:QPaintEvent):    
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            range = (cursor.selectionStart(), cursor.selectionEnd())
            with QPainter(self.editor.viewport()) as painter:
                self.paint_white_sapces(range, painter)

    def paint_white_sapces(self, range:tuple, painter:QPainter):
        cursor = self.editor.textCursor()
        
        cursor.setPosition(range[0])
        first_block = cursor.block()

        cursor.setPosition(range[1], QTextCursor.KeepAnchor)
        last_line = cursor.blockNumber()

        for block in TextEngine.iterate_blocks_from(first_block, last_line):
            text = block.text()
            for column, draw in enumerate(self._chooseVisibleWhitespace(text)):
                if draw:
                    self.drawWhiteSpace(block, column, text[column], painter)

    def drawWhiteSpace(self, block, column, char, painter:QPainter):
        leftCursorRect = TextEngine(self.editor).cursor_rect(block, column, offset=0)
        rightCursorRect = TextEngine(self.editor).cursor_rect(block, column + 1, offset=0)
        if leftCursorRect.top() == rightCursorRect.top():  # if on the same visual line
            middleHeight = (leftCursorRect.top() + leftCursorRect.bottom()) / 2
            if char == ' ':
                painter.setPen(Qt.transparent)
                painter.setBrush(QBrush(Qt.gray))
                xPos = (leftCursorRect.x() + rightCursorRect.x()) / 2
                painter.drawRect(QRect(int(xPos), int(middleHeight), 2, 2))
            else:
                painter.setPen(QColor(Qt.gray).lighter(f=120))
                painter.drawLine(leftCursorRect.x() + 3, middleHeight,
                                    rightCursorRect.x() - 3, middleHeight)
