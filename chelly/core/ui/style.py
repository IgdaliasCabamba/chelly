from __future__ import annotations

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..api import ChellyEditor

from qtpy.QtCore import Qt
from qtpy.QtGui import QPalette, QBrush, QColor
from .themes import ChellyTheme
from typing_extensions import Self

class ChellyStyle:
    
    @property
    def selection_background(self) -> QColor:
        return self._selection_background
    
    @selection_background.setter
    def selection_background(self, color:QColor) -> None:
        if isinstance(color, QColor):
            color = QBrush(color)
        
        if isinstance(color, QBrush):
            self._selection_background = color
            self.update_palette_brush(QPalette.Highlight, self._selection_background)
    
    @property
    def selection_foreground(self) -> QColor:
        return self._selection_foreground
    
    @selection_foreground.setter
    def selection_foreground(self, color:QColor) -> None:
        if isinstance(color, QColor):
            self._selection_foreground = color
            self.update_palette_color(QPalette.HighlightedText, self._selection_foreground)

    def __init__(self, editor) -> None:
        self.editor = editor
        
        _selection_background = QColor(Qt.GlobalColor.darkBlue)
        _selection_background.setAlpha(180)

        self._selection_background = QBrush(_selection_background)
        self._selection_foreground = QColor(Qt.GlobalColor.white)
        self.__mount()
        
    def __mount(self) -> None:
        self.selection_foreground = self._selection_foreground
        self.selection_background = self._selection_background
    
    @property
    def shared_reference(self) -> dict:
        return{
            "selection_background":self.selection_background,
            "selection_foreground":self.selection_foreground,
        }

    def shared_reference(self, other_style:dict) -> Self:
        for key, value in other_style.items():
            if hasattr(self, key):
                try:
                    setattr(self, key, value)
                except AttributeError:
                    pass
    
    # TODO: update all palette

    def update_palette_brush(self, *args, **kargs) -> None:
        palette = self.editor.palette()
        palette.setBrush(*args, **kargs)
        self.editor.setPalette(palette)
    
    def update_palette_color(self, *args, **kargs) -> None:
        palette = self.editor.palette()
        palette.setColor(*args, **kargs)
        self.editor.setPalette(palette)