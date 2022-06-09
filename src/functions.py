class TextFunctions:
    def __init__(self, editor):
        self._editor = editor
    
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
        return self._editor.document().blockCount()

    def get_line_pos_from_number(self, line_number):
        editor = self._editor
        block = editor.document().findBlockByNumber(line_number)
        if block.isValid():
            return int(editor.blockBoundingGeometry(block).translated(
                editor.contentOffset()).top())
        if line_number <= 0:
            return 0
        else:
            return int(editor.blockBoundingGeometry(
                block.previous()).translated(editor.contentOffset()).bottom())

    def get_line_nbr_from_position(self, y_pos):
        editor = self._editor
        height = editor.fontMetrics().height()
        for top, line, block in editor.visible_blocks:
            if top <= y_pos <= top + height:
                return line
        return -1