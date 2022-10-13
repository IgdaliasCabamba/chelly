from qtpy.QtCore import Qt
from qtpy.QtGui import QFontMetrics

#from ..api.chelly import ChellyEditor as CodeEditor
from ..code_editor import CodeEditor
from ...core import TextEngine, Character

class DocumentMap(CodeEditor):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor:CodeEditor = parent.editor
        self._amount_of_blocks = TextEngine(self.editor).line_count
        
        self.zoomOut(8)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setMouseTracking(True)
        self.setTabStopDistance(QFontMetrics(
            self.font()).horizontalAdvance(Character.LARGEST.value))
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
    def mouseMoveEvent(self, event) -> None:
        pass

    def mouseReleaseEvent(self, event) -> None:
        pass

    def wheelEvent(self, event) -> None:
        self.editor.wheelEvent(event)
    
    def _update_contents(self, pos:int=0, charsrem:int=0, charsadd:int=0):
        line_number = TextEngine(self.editor).current_line_nbr
        TextEngine(self).move_cursor_to_line(line_number)
        line_count = TextEngine(self.editor).line_count

        if self._amount_of_blocks == line_count:
            text = TextEngine(self.editor).text_at_line(line_number)
            TextEngine(self).set_text_at_line(
                self.textCursor().blockNumber(), text)
            TextEngine(self).move_cursor_to_line(line_number)
        
        elif self._amount_of_blocks == line_count-1:
            cursor = self.textCursor()
            cursor.setPosition(pos)
            cursor.insertText("\n")
            self.setTextCursor(cursor)
        
        elif self._amount_of_blocks == line_count+1:
            TextEngine(self).move_cursor_to_line(line_number+1)
            cursor = self.textCursor()
            cursor.deletePreviousChar()
            self.setTextCursor(cursor)

        else:
            cursor = self.textCursor()
            cursor.setPosition(pos)
            
            if charsrem:
                for _ in range(charsrem):
                    cursor.deleteChar()

            if charsadd:
                calc = pos + charsadd
                start_block = TextEngine(self.editor).block_from_position(pos)
                end_block = TextEngine(self.editor).block_from_position(calc)
                
                new_blocks = list(TextEngine(self.editor).iterate_blocks_from(start_block, end_block.blockNumber()))
                for nb in new_blocks:
                    cursor.beginEditBlock()
                    cursor.insertText(nb.text())

                    if nb.next().blockNumber() >= 0 and nb != end_block:
                        cursor.insertText("\n")
                    
                    cursor.endEditBlock()
            
            self.setTextCursor(cursor)

            TextEngine(self).move_cursor_to_line(
                TextEngine(self.editor).current_line_nbr
            )

        self._amount_of_blocks = TextEngine(self.editor).line_count