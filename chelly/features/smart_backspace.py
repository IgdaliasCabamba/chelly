from qtpy import QtCore, QtGui
from ..core import Feature


class SmartBackSpace(Feature):
    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.editor.on_key_pressed.connect(self._on_key_pressed)

    def _on_key_pressed(self, event) -> None:
        no_modifiers = int(event.modifiers()) == QtCore.Qt.NoModifier
        if event.key() == QtCore.Qt.Key_Backspace and no_modifiers:
            
            if self.editor.textCursor().atBlockStart():
                return None

            indent_size = self.editor.properties.indent_size
            if self.editor.textCursor().positionInBlock() % indent_size == 0:
                
                # count the number of spaces deletable, stop at tab len
                spaces = 0
                tmp_cursor = QtGui.QTextCursor(self.editor.textCursor())
                while spaces < indent_size or tmp_cursor.atBlockStart():
                    pos = tmp_cursor.position()
                    tmp_cursor.movePosition(tmp_cursor.Left, tmp_cursor.KeepAnchor)
                    char = tmp_cursor.selectedText()
                    if char == " ":
                        spaces += 1
                    else:
                        break
                    tmp_cursor.setPosition(pos - 1)

                cursor = self.editor.textCursor()
                if spaces == 0:
                    return None
            
                cursor.beginEditBlock()
                for _ in range(spaces-1):
                    cursor.deletePreviousChar()
                cursor.endEditBlock()

                self.editor.setTextCursor(cursor)