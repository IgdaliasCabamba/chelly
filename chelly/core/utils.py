"""
"""
from enum import Enum

from typing import Any, Union
from PySide6.QtGui import QTextCursor, QTextBlock, QColor

def drift_color(base_color, factor=110):
    """
    Return color that is lighter or darker than the base color.
    If base_color.lightness is higher than 128, the returned color is darker
    otherwise is is lighter.
    :param base_color: The base color to drift from
    ;:param factor: drift factor (%)
    :return A lighter or darker color.
    """
    base_color = QColor(base_color)
    if base_color.lightness() > 128:
        return base_color.darker(factor)
    else:
        if base_color == QColor('#000000'):
            return drift_color(QColor('#101010'), factor + 20)
        else:
            return base_color.lighter(factor + 10)

class TextEngine:
    def __init__(self, editor):
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
    
    def position_from_point(self, x_pos:int, y_pos:int) -> int:
        height = self._editor.fontMetrics().height()
        for top, line, block in self._editor.visible_blocks:
            if top <= y_pos <= top + height:
                return block.position()
        return 0
    
    def point_y_from_block(self, block) -> int:
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

    def line_number_from_position(self, x_pos:int, y_pos:int) -> int:
        editor = self._editor
        height = editor.fontMetrics().height()
        for top, line, block in editor.visible_blocks:
            if top <= y_pos <= top + height:
                return line
        return -1
    
    def move_cursor_to_block(self, block) -> QTextCursor:
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

    def set_text_at_line(self, line_nbr:int, new_text:str) -> None:
        editor = self._editor
        text_cursor = self.move_cursor_to_line(line_nbr)
        text_cursor.select(text_cursor.LineUnderCursor)
        text_cursor.insertText(new_text)
        editor.setTextCursor(text_cursor)
    
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

class TextBlockHelper(object):
    """
    Helps retrieving the various part of the user state bitmask.
    This helper should be used to replace calls to
    ``QTextBlock.setUserState``/``QTextBlock.getUserState`` as well as
    ``QSyntaxHighlighter.setCurrentBlockState``/
    ``QSyntaxHighlighter.currentBlockState`` and
    ``QSyntaxHighlighter.previousBlockState``.
    The bitmask is made up of the following fields:
        - bit0 -> bit26: User state (for syntax highlighting)
        - bit26: fold trigger state
        - bit27-bit29: fold level (8 level max)
        - bit30: fold trigger flag
        - bit0 -> bit15: 16 bits for syntax highlighter user state (
          for syntax highlighting)
        - bit16-bit25: 10 bits for the fold level (1024 levels)
        - bit26: 1 bit for the fold trigger flag (trigger or not trigger)
        - bit27: 1 bit for the fold trigger state (expanded/collapsed)
    """
    @staticmethod
    def get_state(block):
        """
        Gets the user state, generally used for syntax highlighting.
        :param block: block to access
        :return: The block state
        """
        if block is None:
            return -1
        state = block.userState()
        if state == -1:
            return state
        return state & 0x0000FFFF

    @staticmethod
    def set_state(block, state):
        """
        Sets the user state, generally used for syntax highlighting.
        :param block: block to modify
        :param state: new state value.
        :return:
        """
        if block is None:
            return
        user_state = block.userState()
        if user_state == -1:
            user_state = 0
        higher_part = user_state & 0x7FFF0000
        state &= 0x0000FFFF
        state |= higher_part
        block.setUserState(state)

    @staticmethod
    def get_fold_lvl(block):
        """
        Gets the block fold level
        :param block: block to access.
        :returns: The block fold level
        """
        if block is None:
            return 0
        state = block.userState()
        if state == -1:
            state = 0
        return (state & 0x03FF0000) >> 16

    @staticmethod
    def set_fold_lvl(block, val):
        """
        Sets the block fold level.
        :param block: block to modify
        :param val: The new fold level [0-7]
        """
        if block is None:
            return
        state = block.userState()
        if state == -1:
            state = 0
        if val >= 0x3FF:
            val = 0x3FF
        state &= 0x7C00FFFF
        state |= val << 16
        block.setUserState(state)

    @staticmethod
    def is_fold_trigger(block):
        """
        Checks if the block is a fold trigger.
        :param block: block to check
        :return: True if the block is a fold trigger (represented as a node in
            the fold panel)
        """
        if block is None:
            return False
        state = block.userState()
        if state == -1:
            state = 0
        return bool(state & 0x04000000)

    @staticmethod
    def set_fold_trigger(block, val):
        """
        Set the block fold trigger flag (True means the block is a fold
        trigger).
        :param block: block to set
        :param val: value to set
        """
        if block is None:
            return
        state = block.userState()
        if state == -1:
            state = 0
        state &= 0x7BFFFFFF
        state |= int(val) << 26
        block.setUserState(state)

    @staticmethod
    def is_collapsed(block):
        """
        Checks if the block is expanded or collased.
        :param block: QTextBlock
        :return: False for an open trigger, True for for closed trigger
        """
        if block is None:
            return False
        state = block.userState()
        if state == -1:
            state = 0
        return bool(state & 0x08000000)

    @staticmethod
    def set_collapsed(block, val):
        """
        Sets the fold trigger state (collapsed or expanded).
        :param block: The block to modify
        :param val: The new trigger state (True=collapsed, False=expanded)
        """
        if block is None:
            return
        state = block.userState()
        if state == -1:
            state = 0
        state &= 0x77FFFFFF
        state |= int(val) << 27
        block.setUserState(state)

class Character(Enum):
    SPACE:str = " "
    TAB:str = "\t"
    EMPTY:str = str()
    LARGEST = "W"