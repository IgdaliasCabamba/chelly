from PySide6.QtGui import QColor
from typing_extensions import Self

class ChellyStyle:
    
    class Selection:
        background:QColor = None
        foreground:QColor = None
    
    class Caret:
        background:QColor = None
        foreground:QColor = None
    
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
        self._caret_line = ChellyStyle.Caret()
        self._margin = ChellyStyle.Margin()
        self._indentation_guide = ChellyStyle.IndentationGuide()
    
    @property
    def selection(self) -> Selection:
        return self._selection
    
    @selection.setter
    def selection(self, new_selection) -> None:
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
    def caret_line(self) -> Caret:
        return self._caret_line
    
    @caret_line.setter
    def caret_line(self, new_caret_line) -> None:
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
    def margin(self, new_margin) -> None:
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