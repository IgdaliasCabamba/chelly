from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QColor, QTextFormat, QBrush
from PySide6.QtCore import Qt
from ..core import Feature, TextDecoration, drift_color

class CaretLineHighLighter(Feature):

    @property
    def line_text_color(self) -> bool:
        return self.settings.line_text_color
    
    @line_text_color.setter
    def line_text_color(self, value:bool) -> None:
        self.settings.line_text_color = value

    def __init__(self, editor):
        super().__init__(editor)
        self._decoration = None
        self._pos = -1
        
        self.editor.cursorPositionChanged.connect(self.refresh)
        self.editor.on_text_setted.connect(self.refresh)
        self.refresh()
    
    def _clear_deco(self):
        """ Clear line decoration """
        if self._decoration:
            self.editor.decorations.remove(self._decoration)
            self._decoration = None

    def refresh(self):
        """
        Updates the current line decoration
        """
        self._clear_deco()
        if not self.editor.isReadOnly():
            brush = QBrush(self.editor.style.theme.caret_line_background)
            self._decoration = TextDecoration(self.editor.textCursor())
            self._decoration.set_background(brush)
            self._decoration.set_full_width()
            if self.line_text_color:
                self._decoration.set_foreground(self.editor.style.theme.caret_line_foreground)
            self.editor.decorations.append(self._decoration)