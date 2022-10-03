from typing import Any, Union
from qtpy.QtGui import QTextCursor, QTextBlock, QFont, QFontMetrics

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
    
    def block_from_line_number(self, line_number:int) -> QTextBlock:
        return self._editor.document().findBlockByLineNumber(line_number)
    
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

    def line_number_from_position(self, y_pos:int, x_pos:int=0) -> int:
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
    
    def goto_line(self, line, column=0, move=True):
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