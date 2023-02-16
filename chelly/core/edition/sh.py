from __future__ import annotations

from typing import TYPE_CHECKING, Type, Union

if TYPE_CHECKING:
    from ...api import ChellyEditor

from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QRegularExpression
from qtpy.QtGui import QSyntaxHighlighter, QTextCharFormat, QCursor
from .text_formats import ColorScheme


class Highlighter(QSyntaxHighlighter):
    class HighlightingRule:
        pattern = QRegularExpression()
        format = QTextCharFormat()

    def __init__(self, editor: ChellyEditor):
        super().__init__(editor.document())
        self.__editor = editor

    @property
    def editor(self):
        return self.__editor


class SyntaxHighlighter(Highlighter):
    block_highlight_started = Signal(object, object)
    block_highlight_finished = Signal(object, object)

    @property
    def formats(self):
        return self._color_scheme.formats

    @property
    def color_scheme(self):
        return self._color_scheme

    @color_scheme.setter
    def color_scheme(self, color_scheme):
        if isinstance(color_scheme, ColorScheme):
            self._color_scheme = color_scheme
            self.rehighlight()

    def __init__(self, editor: ChellyEditor, color_scheme: dict = None):
        super().__init__(editor)

        if color_scheme is None:
            color_scheme = dict({})

        self._color_scheme = ColorScheme(color_scheme)

    def highlightBlock(self, text) -> None:
        current_block = self.currentBlock()
        # if current_block.isVisible() and current_block.isValid():
        # self.block_highlight_started.emit(self, current_block)
        self.highlight_block(text, current_block)
        # self.block_highlight_finished.emit(self, current_block)

    def highlight_block(self, text, block) -> None:
        raise NotImplementedError()

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            super().rehighlight()
        except RuntimeError:
            ...
        QApplication.restoreOverrideCursor()


__all__ = ["Highlighter", "SyntaxHighlighter"]
