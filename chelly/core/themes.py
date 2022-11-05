from __future__ import annotations

from typing import TYPE_CHECKING, Type, Union, Any, Dict, List

if TYPE_CHECKING:
    from ..api import ChellyEditor

from string import Template
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QPalette
from typing_extensions import Self
from .utils.helpers import ChellyEvent

class ChellyTheme:
        
    @property
    def selection_background(self) -> QColor:
        return self._selection_background
    
    @selection_background.setter
    def selection_background(self, color:QColor) -> None:
        if isinstance(color, QColor):
            self._selection_background = color
            self.on_palette_changed.emit(QPalette.Highlight, color)
    
    @property
    def selection_foreground(self) -> QColor:
        return self._selection_foreground
    
    @selection_foreground.setter
    def selection_foreground(self, color:QColor) -> None:
        if isinstance(color, QColor):
            self._selection_foreground = color
            self.on_palette_changed.emit(QPalette.HighlightedText, color)

    def __init__(self):
        self.on_palette_changed = ChellyEvent(Any, QColor)

        self._selection_background = QColor(Qt.GlobalColor.darkBlue)
        self._selection_background.setAlpha(180)
        self._selection_foreground = QColor(Qt.GlobalColor.white)
        self.__mount()
        
    def __mount(self) -> None:
        self.selection_foreground = self._selection_foreground
        self.selection_background = self._selection_background