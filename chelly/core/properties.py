from typing import Any
from qtpy.QtGui import QFontMetrics, QTextOption
from qtpy.QtWidgets import QPlainTextEdit

from ..core.utils import Character, FontEngine

class Property:
    class Default:
        INDENT_SIZE = 4

    class Indentation:
        spaces = 0
        tabs = 1

class Properties(object):
    def __init__(self, editor:QPlainTextEdit) -> None:
        self._editor = editor
        self._indent_size:int = Property.Default.INDENT_SIZE
        self._indent_type:int = Property.Indentation.tabs
        self._indent_char:Character = Character.TAB
        self._show_whitespaces:bool = False
        self.__decorations:list = []
    
    @property
    def lines_text(self) -> list:
        return self.text.splitlines()
    
    @property
    def decorations(self):
        return self.__decorations
    
    @property
    def show_whitespaces(self) -> bool:
        return self._show_whitespaces
    
    @property
    def text(self) -> str:
        return self._editor.toPlainText()
    
    @text.setter
    def text(self, text:Any) -> None:
        self._editor.setPlainText(str(text))
    
    @property
    def indent_type(self) -> int:
        return self._indent_type
    
    @property
    def indent_with_tabs(self) -> bool:
        return (self._indent_type == Property.Indentation.tabs)
    
    @property
    def tab_stop_distance(self) -> float:
        return self._editor.tabStopDistance()
    
    @property
    def indent_char(self) -> Character:
        return self._indent_char

    @indent_with_tabs.setter
    def indent_with_tabs(self, tabs:bool) -> None:
        if tabs:
            self._indent_char = Character.TAB
            self._indent_type = Property.Indentation.tabs
        else:
            self._indent_char = Character.SPACE
            self._indent_type = Property.Indentation.spaces
        self.__set_tab_distance(Character.SPACE.value, self.indent_size)
    
    @property
    def indent_with_spaces(self) -> bool:
        return (self._indent_type == Property.Indentation.spaces)

    @indent_with_spaces.setter
    def indent_with_spaces(self, spaces:bool) -> None:
        if spaces:
            self._indent_char = Character.SPACE
            self._indent_type = Property.Indentation.spaces
        else:
            self._indent_char = Character.TAB
            self._indent_type = Property.Indentation.tabs
        self.__set_tab_distance(Character.SPACE.value, self.indent_size)
    
    @property
    def indent_size(self) -> int:
        return self._indent_size
    
    @indent_size.setter
    def indent_size(self, size:int) -> None:
        self._indent_size = size
        self.__set_tab_distance(Character.SPACE.value, size)
    
    def __set_tab_distance(self, char:str, indent_size:int):        
        char_width:float = FontEngine(self._editor.font()).real_horizontal_advance(char, min_zero=True)
        self._editor.setTabStopDistance(char_width * indent_size)

    def default(self):
        self.__set_tab_distance(Character.SPACE.value, self.indent_size)
        self._editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)