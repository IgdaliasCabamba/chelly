from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List

import sys

from typing import Any, Union
from qtpy.QtGui import QFont, QTextOption
from qtpy.QtWidgets import QPlainTextEdit

from .utils import Character, FontEngine
from .base import BaseElement

class PropertyCollections:

    class Default:
        ZOOM_LEVEL = 0
        INDENT_SIZE = 4
        FONT = 'Source Code Pro' if sys.platform != 'darwin' else 'Monaco'

    class Indentation:
        spaces = 0
        tabs = 1

class Properties(BaseElement):
    def __init__(self, editor: QPlainTextEdit) -> None:
        self._editor = editor
        self._indent_size: int = PropertyCollections.Default.INDENT_SIZE
        self._indent_type: int = PropertyCollections.Indentation.tabs
        self._indent_char: Character = Character.TAB
        self._show_whitespaces: bool = False
        self.__decorations: list = []
        self._font: QFont = None
        self._font_size: int = 0  # self._editor.font().pointSize()
        self._font_family: str = PropertyCollections.Default.FONT
        self._zoom: int = 0
        self._view_only = False

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
    def text(self, text: Any) -> None:
        self._editor.setPlainText(str(text))

    @property
    def view_only(self) -> bool:
        return self._view_only

    @view_only.setter
    def view_only(self, value: bool) -> None:
        if isinstance(value, bool):
            self._view_only = value

    @property
    def indent_type(self) -> int:
        return self._indent_type

    @property
    def indent_with_tabs(self) -> bool:
        return (self._indent_type == PropertyCollections.Indentation.tabs)

    @property
    def tab_stop_distance(self) -> float:
        return self._editor.tabStopDistance()

    @property
    def indent_char(self) -> Character:
        return self._indent_char

    @indent_with_tabs.setter
    def indent_with_tabs(self, tabs: bool) -> None:
        if tabs:
            self._indent_char = Character.TAB
            self._indent_type = PropertyCollections.Indentation.tabs
        else:
            self._indent_char = Character.SPACE
            self._indent_type = PropertyCollections.Indentation.spaces
        self.__set_tab_distance(Character.SPACE.value, self.indent_size)

    @property
    def indent_with_spaces(self) -> bool:
        return (self._indent_type == PropertyCollections.Indentation.spaces)

    @indent_with_spaces.setter
    def indent_with_spaces(self, spaces: bool) -> None:
        if spaces:
            self._indent_char = Character.SPACE
            self._indent_type = PropertyCollections.Indentation.spaces
        else:
            self._indent_char = Character.TAB
            self._indent_type = PropertyCollections.Indentation.tabs
        self.__set_tab_distance(Character.SPACE.value, self.indent_size)

    @property
    def indent_size(self) -> int:
        return self._indent_size

    @indent_size.setter
    def indent_size(self, size: int) -> None:
        self._indent_size = size
        self.__set_tab_distance(Character.SPACE.value, size)

    @property
    def font(self) -> QFont:
        return self._font

    @font.setter
    def font(self, new_font: QFont) -> None:
        self._font = new_font
        self._font_size = new_font.pointSize()
        self._editor.setFont(new_font)

    @property
    def font_family(self) -> str:
        return self._font_family

    @font_family.setter
    def font_family(self, new_family: str) -> None:
        self._font_family = new_family
        font = self._editor.font()
        font.setFamily(new_family)
        self._editor.setFont(font)

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, new_size: Union[int, float]) -> None:
        self._font_size = new_size
        font = self._editor.font()

        if isinstance(new_size, int):
            font.setPointSize(new_size)
        elif isinstance(new_size, float):
            font.setPointSizeF(new_size)

        self._editor.setFont(font)

    @property
    def zoom(self) -> int:
        return self._zoom

    @zoom.setter
    def zoom(self, level: Union[int, float]) -> None:
        self._zoom = level
        font_calc = self._font_size + self._zoom

        new_font = QFont(self._font_family)

        if isinstance(level, float):
            if font_calc <= 0:
                new_font.setPointSizeF(self._editor.font().pointSizeF())
            else:
                new_font.setPointSizeF(font_calc)

        elif isinstance(level, int):
            if font_calc <= 0:
                new_font.setPointSize(self._editor.font().pointSize())
            else:
                new_font.setPointSize(font_calc)

        self._editor.setFont(new_font)

    def __set_tab_distance(self, char: str, indent_size: int):
        char_width: float = FontEngine(
            self._editor.font()).real_horizontal_advance(char, min_zero=True)
        self._editor.setTabStopDistance(char_width * indent_size)

    def default(self):
        self.__set_tab_distance(Character.SPACE.value, self.indent_size)
        self._editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)
