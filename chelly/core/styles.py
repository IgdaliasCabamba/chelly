from __future__ import annotations
import string

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api import ChellyEditor

from string import Template
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from typing_extensions import Self

class _StyleElement:
    def __init__(self, editor: ChellyEditor):
        self.__editor = editor

    @property
    def editor(self) -> ChellyEditor:
        return self.__editor


class ChellyStyle:

    class DocumentMap:
        slider_hover_color:tuple = (255, 255, 255, 30)
        slider_color:tuple = (255, 255, 255, 15)
        slider_no_state_color:tuple = (255, 255, 255, 0)
        shadow_color = QColor("#111111")

    class TextEditor(_StyleElement):
        def __init__(self, editor: ChellyEditor):
            super().__init__(editor)
            self.__style_sheet = Template("")

        @property
        def style_sheet(self) -> QColor:
            return self.__style_sheet

        @style_sheet.setter
        def style_sheet(self, new_style_sheet: Template) -> None:
            if isinstance(new_style_sheet, Template):
                pass

    class Selection(_StyleElement):

        def __init__(self, editor:ChellyEditor):
            super().__init__(editor)
            self._background = QColor(Qt.GlobalColor.darkBlue)
            self._background.setAlpha(50)
            self._foreground = QColor(Qt.GlobalColor.white)
            self.__mount()
        
        def __mount(self):
            self.background = self._background
            self.foreground = self._foreground
        
        def clone(self, other_selection):
            self.background = other_selection.background
            self.foreground = other_selection.foreground
        
        @property
        def background(self) -> QColor:
            return self._background
        
        @background.setter
        def background(self, color:QColor):
            if isinstance(color, QColor):
                self._background = color
                palette = self.editor.palette()
                palette.setColor(QPalette.Highlight, self._background)
                self.editor.setPalette(palette)
        
        @property
        def foreground(self) -> QColor:
            return self._foreground
        
        @foreground.setter
        def foreground(self, color:QColor):
            if isinstance(color, QColor):
                self._foreground = color
                palette = self.editor.palette()
                palette.setColor(QPalette.HighlightedText, self._foreground)
                self.editor.setPalette(palette)

    class CaretLine:
        background = QColor(Qt.GlobalColor.darkBlue)
        background.setAlpha(70)
        foreground = QColor(Qt.GlobalColor.white)

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
        color = QColor(Qt.GlobalColor.darkGray)
        active_color = QColor(Qt.GlobalColor.gray)

    def __init__(self, editor:ChellyEditor) -> None:
        self._editor = editor
        self._text_editors = [ChellyStyle.TextEditor(self._editor)]
        self._selections = [ChellyStyle.Selection(self._editor)]
        self._minimap = ChellyStyle.DocumentMap()
        self._caret_line = ChellyStyle.CaretLine()
        self._margins = ChellyStyle.Margins()
        self._indentation_guide = ChellyStyle.IndentationGuide()
        self._lexer_style = None
        self.__others = dict()

    @property
    def others(self) -> dict:
        return self.__others

    def set(self, key: Any, value: Any) -> Self:
        self.__others[key] = value
        return self

    def get(self, key: Any) -> Any:
        return self.__others[key]

    def has(self, key: Any) -> bool:
        if key in self.__others.keys():
            return True
        return False

    def add_editor(self, editor):
        style = ChellyStyle.TextEditor(editor)
        selection = ChellyStyle.Selection(editor)
        selection.clone(self.selection)
        self._text_editors.append(style)
        self._selections.append(selection)

    @property
    def text_editor(self) -> TextEditor:
        # return the main editor
        return self._text_editors[0]

    @text_editor.setter
    def text_editor(self, new_text_editor) -> None:
        self._text_editors.append(new_text_editor)

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
    def minimap_shadow_color(self) -> tuple:
        return self._minimap.shadow_color
    
    @property
    def minimap_slider_color(self) -> tuple:
        return self._minimap.slider_color
    
    @property
    def minimap_slider_hover_color(self) -> tuple:
        return self._minimap.slider_hover_color
    
    @property
    def minimap_slider_no_state_color(self) -> tuple:
        return self._minimap.slider_no_state_color

    @property
    def selection(self) -> Selection:
        return self._selections[0]

    @selection.setter
    def selection(self, new_selection: Selection) -> None:
        self._selections.append(new_selection)

    @property
    def selection_foreground(self) -> QColor:
        return self.selection.foreground

    @selection_foreground.setter
    def selection_foreground(self, color: QColor) -> None:
        for selection in self._selections:
            selection.foreground = color

    @property
    def selection_background(self) -> QColor:
        return self.selection.background

    @selection_background.setter
    def selection_background(self, color: QColor) -> None:
        for selection in self._selections:
            selection.background = color

    @property
    def caret_line(self) -> CaretLine:
        return self._caret_line

    @caret_line.setter
    def caret_line(self, new_caret_line: CaretLine) -> None:
        self._caret = new_caret_line

    @property
    def caret_line_foreground(self) -> QColor:
        return self._caret_line.foreground

    @caret_line_foreground.setter
    def caret_line_foreground(self, color: QColor) -> None:
        self._caret_line.foreground = color

    @property
    def caret_line_background(self) -> QColor:
        return self._caret_line.background

    @caret_line_background.setter
    def caret_line_background(self, color: QColor) -> None:
        self._caret_line.background = color

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

    @property
    def indentation_guide(self) -> IndentationGuide:
        return self._indentation_guide

    @indentation_guide.setter
    def indentation_guide(self, new_indentation_guide) -> None:
        self._indentation_guide = new_indentation_guide

    @property
    def indentation_guide_color(self) -> QColor:
        return self._indentation_guide.color

    @indentation_guide_color.setter
    def indentation_guide_color(self, color: QColor) -> None:
        self._indentation_guide.color = color

    @property
    def indentation_guide_active_color(self) -> QColor:
        return self._indentation_guide.active_color

    @indentation_guide_active_color.setter
    def indentation_guide_active_color(self, color: QColor) -> None:
        self._indentation_guide.active_color = color

    def apply(self) -> Self:
        return self

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