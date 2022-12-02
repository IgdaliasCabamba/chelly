from __future__ import annotations

from typing import TYPE_CHECKING, Union, Any

if TYPE_CHECKING:
    from ..api import ChellyEditor

from qtpy.QtCore import Qt
from qtpy.QtGui import QPalette, QBrush, QColor
from .themes import ChellyTheme
from ...internal import ChellyFollowable, ChellyFollowedValue, chelly_property
from typing_extensions import Self

class ChellyStyle(ChellyFollowable):

    @property
    def name(self):
        return None

    
    @chelly_property
    def selection_background(self) -> QColor:
        return self._selection_background
    
    @selection_background.setter
    def selection_background(self, color:Union[QBrush, QColor]) -> None:
        if isinstance(color, QColor):
            color = QBrush(color)
        
        if isinstance(color, QBrush):
            self._selection_background = color
            self.update_palette_brush(QPalette.Highlight, self._selection_background)
    
    @selection_background.follower
    def selection_background(self, origin:Self, value:Any):
        for editor in self.editor.followers:
            editor.style.selection_background = ChellyFollowedValue(value)
    
    @chelly_property
    def selection_foreground(self) -> QColor:
        return self._selection_foreground
    
    @selection_foreground.setter
    def selection_foreground(self, color:QColor) -> None:

        if isinstance(color, QColor):
            self._selection_foreground = color
            self.update_palette_color(QPalette.HighlightedText, self._selection_foreground)

    @selection_foreground.follower
    def selection_foreground(self, origin:Self, value:Any):
        for editor in self.editor.followers:
            editor.style.selection_foreground = ChellyFollowedValue(value)

    def __init__(self, editor) -> None:
        super().__init__(editor)
        
        _sel_bg = QColor(Qt.GlobalColor.darkBlue)
        _sel_bg.setAlpha(180)

        self._selection_background = QBrush(_sel_bg)
        self._selection_foreground = QColor(Qt.GlobalColor.white)

        self.selection_background = self._selection_background
        self.selection_foreground = self._selection_foreground

    def update_palette_brush(self, *args, **kargs) -> None:
        palette = self.editor.palette()
        palette.setBrush(*args, **kargs)
        self.editor.setPalette(palette)
    
    def update_palette_color(self, *args, **kargs) -> None:
        palette = self.editor.palette()
        palette.setColor(*args, **kargs)
        self.editor.setPalette(palette)
    
    def follow(self, other_style):
        self.selection_background = other_style.selection_background
        self.selection_foreground = other_style.selection_foreground