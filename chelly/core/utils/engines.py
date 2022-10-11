from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Union, Any
from qtpy.QtGui import QTextCursor, QTextBlock, QFont, QFontMetrics
from qtpy.QtCore import QRect
import enum

if TYPE_CHECKING:
    from ...api import ChellyEditor    

class TextEngine:
    
    class TextDirection(enum.Enum):
        LEFT = 0
        RIGHT = 1
        UNDER = 2
    
    @property
    def editor(self):
        return self._editor

    def __init__(self, editor:ChellyEditor):
        self._editor = editor
    
    @property
    def first_visible_line(self) -> int:
        return self._editor.firstVisibleBlock().firstLineNumber()
    
    @property
    def visible_lines(self) -> int:
        editor = self._editor
        return(len(editor.visible_blocks))
    
    @property
    def selected_text(self):
        return self._editor.textCursor().selectedText()
    
    @property
    def selection_range(self) -> tuple:
        ...
    
    @property
    def selection_range(self) -> tuple:
        cursor = self._editor.textCursor()
        if cursor.hasSelection():
            return (cursor.selectionStart(), cursor.selectionEnd())
        return None
    
    @property
    def cursor_position(self):
        return (self._editor.textCursor().blockNumber(),
                self._editor.textCursor().columnNumber())
    
    @property
    def current_line_nbr(self):
        return self.cursor_position[0]
    
    @property
    def current_column_nbr(self):
        return self.cursor_position()[1]

    @property
    def line_count(self):
        return self._editor.document().lineCount()
    
    @property
    def block_count(self):
        return self._editor.document().blockCount()
    
    # TODO : compute this
    @property
    def visible_lines_from_line_count(self):
        count = self.line_count
        return count
    
    def blocks_from_selection_range(self, start:int, end:int = None) -> Tuple[QTextBlock, QTextBlock]:
        cursor = self._editor.textCursor()
        
        cursor.setPosition(start)
        first_block = cursor.block()

        cursor.setPosition(end, QTextCursor.KeepAnchor)
        last_block = cursor.block()

        return first_block, last_block
    
    def block_from_line_number(self, line_number:int) -> QTextBlock:
        return self._editor.document().findBlockByLineNumber(line_number)
    
    def position_from_point(self, x_pos:int, y_pos:int) -> int:
        height = self._editor.fontMetrics().height()
        for top, line, block in self._editor.visible_blocks:
            if top <= y_pos <= top + height:
                return block.position()
        return 0
    
    def point_y_from_block(self, block: QTextBlock) -> int:
        if block.isValid():
            return int(self._editor.blockBoundingGeometry(block).translated(
                self._editor.contentOffset()).top())
        else:
            return int(self._editor.blockBoundingGeometry(
                block.previous()).translated(self._editor.contentOffset()).bottom())
    
    def point_y_from_position(self, pos:int) -> int:
        block = self._editor.document().findBlock(pos)
        return self.point_y_from_block(block)

    def point_y_from_line_number(self, line_number:int) -> int:
        block = self._editor.document().findBlockByNumber(line_number)
        if line_number <= 0:
            return 0
        else:
            return self.point_y_from_block(block)

    def line_number_from_position(self, y_pos:int, x_pos:int=0) -> int:
        editor = self._editor
        height = editor.fontMetrics().height()
        for top, line, block in editor.visible_blocks:
            if top <= y_pos <= top + height:
                return line
        return -1
    
    def text_at_line(self, line_nbr:int) -> str:
        if line_nbr is None:
            return str()
        doc = self._editor.document()
        block = doc.findBlockByLineNumber(line_nbr)
        return block.text()
    
    def line_indent(self, line_number:Union[QTextBlock, None]=None, indent_char:str="\t") -> int:
        """
        Returns the indent level of the specified line
        :param line_number: Number of the line to get indentation (1 base).
            Pass None to use the current line number. Note that you can also
            pass a QTextBlock instance instead of an int.
        :return: Number of spaces that makes the indentation level of the
                 current line
        """
        if line_number is None:
            line_number = self.current_line_nbr

        elif isinstance(line_number, QTextBlock):
            line_number = line_number.blockNumber()

        line = self.text_at_line(line_number)
        indentation_level = len(line) - len(line.lstrip(indent_char))
        return indentation_level
    
    def word_at(self, direction:TextDirection = TextDirection.RIGHT, cursor:QTextCursor=None) -> str:
        """
        Gets the character on the given direction of the text cursor.
        :param cursor: QTextCursor where the search will start.
        :return: The word that is on the right of the text cursor.
        """
        if cursor is None:
            cursor = self._editor.textCursor()
        
        if direction == TextEngine.TextDirection.UNDER:
            cursor.movePosition(QTextCursor.WordUnderCursor, QTextCursor.KeepAnchor)

        elif direction == TextEngine.TextDirection.LEFT:
            cursor.movePosition(QTextCursor.WordLeft, QTextCursor.KeepAnchor)
        elif direction == TextEngine.TextDirection.RIGHT:
            cursor.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor)

        return cursor.selectedText()

    def character_at(self, direction:TextDirection = TextDirection.RIGHT, cursor:QTextCursor=None) -> str:
        """
        Gets the character that is on the given direction of the text cursor.
        :param cursor: QTextCursor that defines the position where the search will start.
        """
        next_char = self.word_at(direction, cursor).strip()
        if len(next_char) > 0:
            return next_char[0]
        return None
    
    @staticmethod
    def iterate_blocks_from(block:QTextBlock, until_line:int = None):
        """Generator, which iterates QTextBlocks from block until the End of a document
        """
        while block.isValid():
            yield block
            if block.blockNumber() == until_line:
                break
            block = block.next()

    @staticmethod
    def iterate_blocks_back_from(block:QTextBlock, until_line:int = None):
        """Generator, which iterates QTextBlocks from block until the Start of a document
        """
        while block.isValid():
            yield block
            if block.blockNumber() == until_line:
                break
            block = block.previous()
    
    @staticmethod
    def set_position_in_block(cursor:QTextCursor, position_in_block:int, anchor:QTextCursor.MoveMode = QTextCursor.MoveAnchor):
        return cursor.setPosition(cursor.block().position() + position_in_block, anchor)
    
    @staticmethod
    def previous_non_blank_block(current_block:QTextBlock) -> Union[QTextBlock, None]:
        if current_block.blockNumber():
            previous_block = current_block.previous()
        else:
            previous_block = None

        # find the previous non-blank block
        while (previous_block and previous_block.blockNumber() and previous_block.text().strip() == ''):
            previous_block = previous_block.previous()
        return previous_block

    # Cursor
    
    def move_cursor(self, keep_anchor=False, nb_chars=1):
        """
        Moves the cursor on the right.
        :param keep_anchor: True to keep anchor (to select text) or False to
            move the anchor (no selection)
        :param nb_chars: Number of characters to move.
        """
        text_cursor = self._editor.textCursor()
        text_cursor.movePosition(
            text_cursor.Right, text_cursor.KeepAnchor if keep_anchor else
            text_cursor.MoveAnchor, nb_chars)
        self._editor.setTextCursor(text_cursor)
    
    def move_cursor_to_block(self, block:QTextBlock) -> QTextCursor:
        text_cursor = self._editor.textCursor()
        text_cursor.setPosition(block.position())
        return text_cursor
    
    def move_cursor_to_line(self, line) -> QTextCursor:
        block = self._editor.document().findBlockByLineNumber(line)
        text_cursor = self.move_cursor_to_block(block)
        text_cursor.movePosition(text_cursor.StartOfLine, text_cursor.MoveAnchor)
        self._editor.setTextCursor(text_cursor)
        return text_cursor
    
    def move_cursor_to_position(self, line:int, column:int=0) -> QTextCursor:
        text_cursor = self._editor.textCursor()
        block = self._editor.document().findBlockByLineNumber(line)
        self.move_cursor_to_block(block)
        if column:
            text_cursor.movePosition(text_cursor.Right, text_cursor.MoveAnchor, column)
        
        return text_cursor
 
    def cursor_rect(self, line_or_block:Union[QTextBlock, int], column:int, offset:int) -> QRect:
        block = line_or_block
        if isinstance(line_or_block, int):
            block = self.block_from_line_number(line_or_block)
        
        cursor = QTextCursor(block)
        self.set_position_in_block(cursor, column)
        return self._editor.cursorRect(cursor).translated(offset, 0)
    
    def set_text_at_line(self, line_nbr:int, new_text:str) -> None:
        editor = self._editor
        text_cursor = self.move_cursor_to_line(line_nbr)
        text_cursor.select(text_cursor.LineUnderCursor)
        text_cursor.insertText(new_text)
        editor.setTextCursor(text_cursor)

    def insert_text(self, text:str, keep_position:bool=True):
        """
        Inserts text at the cursor position.
        :param text: text to insert
        :param keep_position: Flag that specifies if the cursor position must
            be kept. Pass False for a regular insert (the cursor will be at
            the end of the inserted text).
        """
        text_cursor = self._editor.textCursor()
        
        if keep_position:
            selection_start = text_cursor.selectionStart()
            selection_end = text_cursor.selectionEnd()

        text_cursor.insertText(text)
        if keep_position:
            text_cursor.setPosition(selection_start)
            text_cursor.setPosition(selection_end, text_cursor.KeepAnchor)
        self._editor.setTextCursor(text_cursor)

    def clear_selection(self) -> None:
        """
        Clears text cursor selection
        """
        text_cursor = self._editor.textCursor()
        text_cursor.clearSelection()
        self._editor.setTextCursor(text_cursor)

    def goto_line(self, line:int, column:int=0, move:bool=True) -> None:
        text_cursor = self.move_cursor_to_line(line)
        if column:
            text_cursor.movePosition(text_cursor.Right, text_cursor.MoveAnchor,
                                     column)
        if move:
            self._editor.setTextCursor(text_cursor)
        return text_cursor
    

class FontEngine:
    def __init__(self, font:QFont):
        self._font = font
        self._metrics = QFontMetrics(self._font)
    
    @property
    def metrics(self):
        return self._metrics
    
    def real_horizontal_advance(self, char:str, min_zero:bool=False) -> float:

        margin_left:int = self.metrics.leftBearing(char)
        margin_right:int = self.metrics.rightBearing(char)

        if min_zero:
            bearing_left:int = 0 if margin_left < 0 else margin_left
            bearing_right:int = 0 if margin_right < 0 else margin_right
            return (self.metrics.horizontalAdvance(char) + bearing_left + bearing_right)
        
        return (self.metrics.horizontalAdvance(char) + margin_left + margin_right)