from typing import Any
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from typing_extensions import Self

class ChellyStyle:
    
    class Selection:
        background = QColor(Qt.GlobalColor.darkBlue)
        background.setAlpha(70)
        foreground = QColor(Qt.GlobalColor.white)
    
    class CaretLine:
        background = QColor(Qt.GlobalColor.darkBlue)
        background.setAlpha(70)
        foreground = QColor(Qt.GlobalColor.white)
    
    class Margin:
        background:QColor = None
        foreground:QColor = None
        highlight:QColor = None
    
    class IndentationGuide:
        color:QColor = None
        width:int = None
    
    def __init__(self, editor) -> None:
        self._editor = editor
        self._selection = ChellyStyle.Selection()
        self._caret_line = ChellyStyle.CaretLine()
        self._margin = ChellyStyle.Margin()
        self._indentation_guide = ChellyStyle.IndentationGuide()
        self._lexer_style = None
        self.__others = dict()
    
    @property
    def others(self) -> dict:
        return self.__others
    
    def set(self, key:Any, value:Any) -> Self:
        self.__others[key] = value
        return self
    
    def get(self, key:Any) -> Any:
        return self.__others[key]
    
    def has(self, key:Any) -> bool:
        if key in self.__others.keys():
            return True
        return False
    
    @property
    def lexer_style(self) -> Any:
        return self._lexer_style
    
    @lexer_style.setter
    def lexer_style(self, new_lexer_style:Any) -> None:
        self._lexer_style = new_lexer_style
        
    @property
    def selection(self) -> Selection:
        return self._selection
    
    @selection.setter
    def selection(self, new_selection:Selection) -> None:
        self._selection = new_selection
    
    @property
    def selection_foreground(self) -> QColor:
        return self._selection.foreground
    
    @selection_foreground.setter
    def selection_foreground(self, color:QColor) -> None:
        self._selection.foreground = color
    
    @property
    def selection_background(self) -> QColor:
        return self._selection.background
    
    @selection_background.setter
    def selection_background(self, color:QColor) -> None:
        self._selection.background = color
    
    @property
    def caret_line(self) -> CaretLine:
        return self._caret_line
    
    @caret_line.setter
    def caret_line(self, new_caret_line:CaretLine) -> None:
        self._caret = new_caret_line
    
    @property
    def caret_line_foreground(self) -> QColor:
        return self._caret_line.foreground
    
    @caret_line_foreground.setter
    def caret_line_foreground(self, color:QColor) -> None:
        self._caret_line.foreground = color
    
    @property
    def caret_line_background(self) -> QColor:
        return self._caret_line.background
    
    @caret_line_background.setter
    def caret_line_background(self, color:QColor) -> None:
        self._caret_line.background = color

    @property
    def margin(self) -> Margin:
        return self._margin
    
    @margin.setter
    def margin(self, new_margin:Margin) -> None:
        self._margin = new_margin
    
    @property
    def margin_foreground(self) -> QColor:
        return self._margin.foreground
    
    @margin_foreground.setter
    def margin_foreground(self, color:QColor) -> None:
        self._margin.foreground = color
    
    @property
    def margin_background(self) -> QColor:
        return self._margin.background
    
    @margin_background.setter
    def margin_background(self, color:QColor) -> None:
        self._margin.background = color
    
    @property
    def margin_highlight(self) -> QColor:
        return self._margin.highlight
    
    @margin_highlight.setter
    def margin_highlight(self, color:QColor) -> None:
        self._margin.highlight = color
    
    @property
    def indentation_guide(self) -> IndentationGuide:
        return self._indentation_guide
    
    @indentation_guide.setter
    def indentation_guide(self, new_indentation_guide) -> None:
        self._indentation_guide = new_indentation_guide
    
    @property
    def indentation_guide_foreground(self) -> QColor:
        return self._indentation_guide.foreground
    
    @indentation_guide_foreground.setter
    def indentation_guide_foreground(self, color:QColor) -> None:
        self._indentation_guide.foreground = color
    
    @property
    def indentation_guide_background(self) -> QColor:
        return self._indentation_guide_background.background
    
    @indentation_guide_background.setter
    def indentation_guide_background(self, color:QColor) -> None:
        self._indentation_guide_background.background = color
    
    '''
    @property
    def (self) -> :
        return self._
    
    @.setter
    def (self, new_) -> None:
        self._ = new_
    
    @property
    def (self) -> QColor:
        return self._.foreground
    
    @.setter
    def (self, color:QColor) -> None:
        self..foreground = color
    
    @property
    def (self) -> QColor:
        return self._.background
    
    @.setter
    def (self, color:QColor) -> None:
        self._.background = color
    '''