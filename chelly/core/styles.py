from __future__ import annotations

from typing import TYPE_CHECKING, Type, Union

if TYPE_CHECKING:
    from ..api import ChellyEditor

from string import Template
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
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

    class DocumentMap:
        
        class Slider:
            _hover_color:tuple = (255, 255, 255, 30)
            _color:tuple = (255, 255, 255, 15)
            _no_state_color:tuple = (255, 255, 255, 0)

            @property
            def color(self) -> tuple:
                return self._color
        
            @color.setter
            def color(self, new_color:tuple) -> None:
                self._color = new_color

            @property
            def no_state_color(self) -> tuple:
                return self._no_state_color
            
            @no_state_color.setter
            def no_state_color(self, new_color:QColor) -> None:
                self._no_state_color = new_color
            
            @property
            def hover_color(self) -> tuple:
                return self._hover_color
        
            @hover_color.setter
            def hover_color(self, new_color:QColor) -> None:
                self._hover_color = new_color


        _slider = Slider()
        _shadow_color = QColor("#111111")
    
        @property
        def shadow_color(self) -> tuple:
            return self._shadow_color
        
        @shadow_color.setter
        def shadow_color(self, new_color:QColor) -> tuple:
            self._shadow_color = new_color
        
        @property
        def slider(self) -> ChellyStyle.DocumentMap.Slider:
            return self._slider
        
        @slider.setter
        def slider(self, new_slider:ChellyStyle.DocumentMap.Slider) -> None:
            self._slider = new_slider

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

    class CaretLine:
        _background = QColor(Qt.GlobalColor.darkBlue)
        _background.setAlpha(70)
        _foreground = QColor(Qt.GlobalColor.white)
        
        @property
        def foreground(self) -> QColor:
            return self._foreground

        @foreground.setter
        def foreground(self, new_color: QColor) -> None:
            self._foreground = new_color

        @property
        def background(self) -> QColor:
            return self._background

        @background.setter
        def background(self, new_color: QColor) -> None:
            self._background = new_color

    class Margins:

        class Colors:
            background = QColor(Qt.GlobalColor.transparent)
            foreground = QColor(Qt.GlobalColor.darkGray)
            highlight = QColor(Qt.GlobalColor.lightGray)

        def __init__(self) -> None:
            self.__items = dict()

        @property
        def items(self) -> dict:
            return self.__items

        def new(self, margin, **kvargs):
            margin_style = ChellyStyle.Margins.Colors()
            margin_style.background = kvargs.get(
                "background", QColor(Qt.GlobalColor.transparent))
            margin_style.background = kvargs.get(
                "foreground", QColor(Qt.GlobalColor.darkGray))
            margin_style.highlight = kvargs.get(
                "highlight", QColor(Qt.GlobalColor.lightGray))
            self.__items[margin] = margin_style

        def __get_margin_style(self, margin: Any) -> Colors:

            if not isinstance(margin, str):
                margin = margin.__name__

            if margin in self.items.keys():
                return self.items[margin]
            else:
                self.new(margin)
                return self.items[margin]

        def get(self, margin, key: Any = None):
            margin_style = self.__get_margin_style(margin)

            if key is None:
                return margin_style
            else:
                return getattr(margin_style, key, QColor(Qt.GlobalColor.transparent))

        def set(self, margin, key, value) -> None:
            margin_style = self.__get_margin_style(margin)
            if margin_style is not None:
                setattr(margin_style, key, value)

    class IndentationGuide:
        _color = QColor(Qt.GlobalColor.darkGray)
        _active_color = QColor(Qt.GlobalColor.gray)

        @property
        def color(self) -> QColor:
            return self._color

        @color.setter
        def color(self, new_color: QColor) -> None:
            self._color = new_color

        @property
        def active_color(self) -> QColor:
            return self._active_color

        @active_color.setter
        def active_color(self, new_color: QColor) -> None:
            self._active_color = new_color


    def __init__(self, editor:ChellyEditor) -> None:
        self._editor = editor

        selection = ChellyStyle.Selection(self._editor)
        selection.on_changed.connect(self._update_selection)
        self._selections = [selection]

        self._minimap = ChellyStyle.DocumentMap()
        self._caret_line = ChellyStyle.CaretLine()
        self._margins = ChellyStyle.Margins()
        self._indentation_guide = ChellyStyle.IndentationGuide()
        self._lexer_style = None
        self.__others = dict()

    @property
    def lexer_style(self) -> Any:
        return self._lexer_style

    @lexer_style.setter
    def lexer_style(self, new_lexer_style: Any) -> None:
        self._lexer_style = new_lexer_style
    
    @property
    def minimap(self) -> DocumentMap:
        return self._minimap
    
    @minimap.setter
    def minimap(self, new_minimap: DocumentMap) -> None:
        self._minimap = new_minimap

    @property
    def selection(self) -> Selection:
        return self._selections[0]

    @selection.setter
    def selection(self, new_selection: Selection) -> None:
        self._selections.append(new_selection)

    @property
    def caret_line(self) -> CaretLine:
        return self._caret_line

    @caret_line.setter
    def caret_line(self, new_caret_line: CaretLine) -> None:
        self._caret = new_caret_line
    
    @property
    def indentation_guide(self) -> IndentationGuide:
        return self._indentation_guide

    @indentation_guide.setter
    def indentation_guide(self, new_indentation_guide) -> None:
        self._indentation_guide = new_indentation_guide

    def set_margin_style(self, margin: Any, **kvargs) -> Self:
        self._margins.new(margin, **kvargs)
        return self

    def margin_style(self, margin) -> dict:
        return self._margins.get(margin, None)

    def set_margin_foreground(self, margin: Any, color: QColor) -> Self:
        margin = self._margins.set(margin, "foreground", color)
        return self

    def margin_foreground(self, margin: Any) -> QColor:
        return self._margins.get(margin, "foreground")

    def set_margin_highlight(self, margin: Any, color: QColor) -> Self:
        margin = self._margins.set(margin, "highlight", color)
        return self

    def margin_highlight(self, margin: Any) -> QColor:
        return self._margins.get(margin, "highlight")

    def set_margin_background(self, margin: Any, color: QColor) -> Self:
        margin = self._margins.set(margin, "background", color)
        return self

    def margin_background(self, margin: Any) -> QColor:
        return self._margins.get(margin, "background")

    def apply(self) -> Self:
        return self
    
    def set(self, key: Any, value: Any) -> Self:
        self.__others[key] = value
        return self

    def get(self, key: Any = None) -> Union[Any, dict]:
        if key is None:
            return self.__others

        return self.__others[key]

    def has(self, key: Any) -> bool:
        if key in self.__others.keys():
            return True
        return False

    def add_editor(self, editor):
        selection = ChellyStyle.Selection(editor)
        selection.clone(self.selection)
        selection.on_changed.connect(self._update_selection)
        self._selections.append(selection)
    
    def _update_selection(self, changed_selection):
        for selection in self._selections:
            if selection is not changed_selection:
                selection.clone(changed_selection)