"""
"""

from PySide6.QtGui import QTextCursor

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