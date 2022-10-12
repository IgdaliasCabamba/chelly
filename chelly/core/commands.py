from __future__ import annotations
from typing import TYPE_CHECKING, Union, Any
from .properties import Property

if TYPE_CHECKING:
    from ..api import ChellyEditor


class BasicCommands:
    def __init__(self, editor:ChellyEditor) -> None:
        self.__editor = editor
    
    @property
    def editor(self):
        return self.__editor
    
    def indent(self):
        cursor = self.editor.textCursor()
        if self.editor.properties.indent_with_spaces:
            cursor.insertText(
                self.editor.properties.indent_char.value * self.editor.properties.indent_size)
        else:
            cursor.insertText(self.editor.properties.indent_char.value)
        
    def un_indent(self):
        ...
        
    def home_key(self, *args, **kwargs):
        ...
    
    def zoom_in(self, range_:int = 1):
        level = self.editor.properties.zoom
        level += range_
        self.editor.properties.zoom = level
    
    def zoom_out(self, range_:int):
        level = self.editor.properties.zoom
        level -= range_
        
        if level < 0:
            level = 1
            
        self.editor.properties.zoom = level
    
    def reset_zoom(self):
        self.editor.properties.zoom = Property.Default.ZOOM_LEVEL