from typing import Any
from xml.dom.minidom import CharacterData
from PySide6.QtGui import QFontMetrics, QTextOption
from ..core.utils import Character

class Property:
    class Default:
        INDENT_SIZE = 4

    class Indentation:
        spaces = 0
        tabs = 1

class Properties(object):
    def __init__(self, editor) -> None:
        self._editor = editor
        self._indent_size:int = Property.Default.INDENT_SIZE
        self._indent_type:int = Property.Indentation.tabs
        self._indent_char:Character = Character.TAB
        self._show_whitespaces:bool = False
    
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
    def document(self) -> object:
        return self._editor.document()
    
    @document.setter
    def document(self, qtextdocument:Any) -> None:
        self._editor.setDocument(qtextdocument)
    
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
        #print(f"margin-left: {QFontMetrics(self._editor.font()).leftBearing(char)} on Spaces:{self.indent_with_spaces}")
        #print(f"margin-right: {QFontMetrics(self._editor.font()).rightBearing(char)} on Spaces:{self.indent_with_spaces}")
        
        metrics = QFontMetrics(self._editor.font())

        margin_left:int = metrics.leftBearing(char)
        margin_right:int = metrics.rightBearing(char)
        bearing_left:int = 0 if margin_left < 0 else margin_left
        bearing_right:int = 0 if margin_right < 0 else margin_right

        char_width:float = (metrics.horizontalAdvance(char) + bearing_left + bearing_right)
        self._editor.setTabStopDistance(char_width * indent_size)

    def default(self):
        self.__set_tab_distance(Character.SPACE.value, self.indent_size)
        self._editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)