from qtpy.QtGui import QKeyEvent, QTextCursor
from qtpy.QtCore import Qt
from ..core import Feature, TextEngine
import string

class AutoComplete(Feature):
    __BASE_KEY_MAP = {'"': '"', "'": "'"}
    KEY_MAP = {**__BASE_KEY_MAP, **{"(": ")", "{": "}", "[": "]"}}
    REVERSED_KEY_MAP = {**__BASE_KEY_MAP, **{")":"(", "}":"{", "]":"["}}

    def __init__(self, editor):
        super().__init__(editor)
        
        self.editor.on_key_pressed.connect(self._on_key_pressed)
        self.editor.post_on_key_pressed.connect(self._post_on_key_pressed)
        
        self.__delete_last_char = False
    
    def _post_on_key_pressed(self, event:QKeyEvent) -> None:
        cursor = self.editor.textCursor()

        if self.__delete_last_char:
            cursor.deletePreviousChar()
            self.__delete_last_char = False
            return None
    
    def _on_key_pressed(self, event:QKeyEvent) -> None:
        cursor = self.editor.textCursor()
        open_char = event.text()
        next_char = TextEngine(self.editor).character_at(direction = TextEngine.TextDirection.RIGHT)
        close_char = AutoComplete.KEY_MAP.get(open_char, None)
        
        if event.key() == Qt.Key_Backspace:
            if next_char in AutoComplete.REVERSED_KEY_MAP.keys():
                
                cursor.movePosition(cursor.Left)
                cursor.movePosition(cursor.Right, cursor.KeepAnchor)
                del_char = cursor.selectedText()

                if AutoComplete.REVERSED_KEY_MAP.get(next_char) == del_char:
                    cursor.deleteChar()

        elif open_char in AutoComplete.KEY_MAP.keys():
            
            if close_char is None:
                return None

            if cursor.hasSelection():
                cursor.insertText(f"{open_char}{cursor.selectedText()}{close_char}")
                self.editor.setTextCursor(cursor)
                self.__delete_last_char = True
            
            elif next_char is None or not next_char.isalnum():
                TextEngine(self.editor).insert_text(close_char)