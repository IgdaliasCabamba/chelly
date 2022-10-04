from qtpy.QtGui import QKeyEvent
from qtpy.QtCore import Qt
from ..core import Feature, TextEngine
import string

class AutoComplete(Feature):
    
    KEY_MAP = {'"': '"', "'": "'", "(": ")", "{": "}", "[": "]"}

    def __init__(self, editor):
        super().__init__(editor)
        self.editor.on_key_pressed.connect(self._on_key_pressed)
    
    def _on_key_pressed(self, event:QKeyEvent):
        cursor = self.editor.textCursor()
        open_char = event.text()
        next_char = TextEngine(self.editor).get_right_character()
        close_char = AutoComplete.KEY_MAP.get(open_char, None)

        if event.key() == Qt.Key_Backspace:
            ...
        
        if close_char is None:
            return None

        if cursor.hasSelection():
            cursor.insertText(f"{open_char}{cursor.selectedText()}{close_char}")
            self.editor.setTextCursor(cursor)
            event.accept()
            return None
        
        elif next_char is None or not next_char.isalnum():
            TextEngine(self.editor).insert_text(close_char)