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

class _StyleElement:
    
    class Palette:
        def __init__(self, editor:ChellyEditor):
            self._editor = editor
            self._palette = editor.palette()
        
        def set_color(self, *args, **kargs):
            self._palette.setColor(*args, **kargs)
            self._editor.setPalette(self._palette)
    
    def __new__(cls: type[Self], *args, **kvargs) -> Self:
        obj = super().__new__(cls)
        obj.on_changed = ChellyEvent(object)
        return obj

    def __init__(self, editor: ChellyEditor):
        self.__palette = _StyleElement.Palette(editor)
        self.__editor = editor
    
    @property
    def palette(self) -> _StyleElement.Palette:
        return self.__palette
    
    @palette.setter
    def palette(self, new_palette:_StyleElement.Palette) -> _StyleElement.Palette:
        self.__palette = new_palette

    @property
    def editor(self) -> ChellyEditor:
        return self.__editor

class ChellyStyle:

    class Selection(_StyleElement):

        def __init__(self, editor:ChellyEditor) -> None:
            super().__init__(editor)
            self._background = QColor(Qt.GlobalColor.darkBlue)
            self._background.setAlpha(50)
            self._foreground = QColor(Qt.GlobalColor.white)
            self.__mount(self)
        
        def __mount(self, selection: ChellyStyle.Selection) -> Self:
            self.__set_bg(selection.background)
            self.__set_fg(selection.foreground)
            return self

        def clone(self, other_selection: ChellyStyle.Selection) -> Self:
            return self.__mount(other_selection)
        
        def __set_bg(self, color:QColor) -> None:
            self._background = color
            self.palette.set_color(QPalette.Highlight, self._background)
        
        def __set_fg(self, color:QColor) -> None:
            self._foreground = color
            self.palette.set_color(QPalette.HighlightedText, self._foreground)
        
        @property
        def background(self) -> QColor:
            return self._background
        
        @background.setter
        def background(self, color:QColor):
            if isinstance(color, QColor):
                self.__set_bg(color)
                self.on_changed.emit(self)
        
        @property
        def foreground(self) -> QColor:
            return self._foreground
        
        @foreground.setter
        def foreground(self, color:QColor):
            if isinstance(color, QColor):
                self.__set_fg(color)
                self.on_changed.emit(self)

    def __init__(self, editor:ChellyEditor) -> None:
        self._editor = editor
        selection = ChellyStyle.Selection(self._editor)
        selection.on_changed.connect(self._update_selection)
        self._selections = [selection]

    @property
    def selection(self) -> Selection:
        return self._selections[0]

    @selection.setter
    def selection(self, new_selection: Selection) -> None:
        self._selections.append(new_selection)
    
    def add_editor(self, editor):
        selection = ChellyStyle.Selection(editor)
        selection.clone(self.selection)
        selection.on_changed.connect(self._update_selection)
        self._selections.append(selection)
    
    def _update_selection(self, changed_selection):
        for selection in self._selections:
            if selection is not changed_selection:
                selection.clone(changed_selection)