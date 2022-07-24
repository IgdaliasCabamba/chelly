from typing import Any
from PySide6.QtGui import QFontMetrics, QTextOption
from dataclasses import dataclass

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
        self._indent_type:int = False
    
    @property
    def text(self) -> str:
        return self._editor.toPlainText()
    
    @text.setter
    def text(self, text:Any) -> None:
        print(text)
        self._editor.setPlainText(str(text))
    
    @property
    def indent_type(self) -> int:
        return self._indent_type

    @indent_type.setter
    def indent_type(self, indentation_type:int) -> None:
        self._indent_type = indentation_type
    
    @property
    def indent_size(self) -> int:
        return self._indent_size
    
    @indent_size.setter
    def indent_size(self, size:int) -> None:
        self._indent_size = size

    def default(self):
        self._editor.setTabStopDistance(QFontMetrics(
            self._editor.font()).horizontalAdvance(' ') * 4)

        self._editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)