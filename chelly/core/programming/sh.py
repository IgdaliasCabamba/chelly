from typing import Union
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QCursor
from .text_formats import ColorScheme

class Highlighter(QSyntaxHighlighter):

    class HighlightingRule():
        pattern = QRegularExpression()
        format = QTextCharFormat()

    def __init__(self, editor):
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

    def __init__(self, editor, color_scheme:dict=None):
        super().__init__(editor)

        if color_scheme is None:
            color_scheme = dict({})

        self._color_scheme = ColorScheme(color_scheme)

    def highlightBlock(self, text):
        current_block = self.currentBlock()
        self.block_highlight_started.emit(self, current_block)
        self.highlight_block(text, current_block)
        self.block_highlight_finished.emit(self, current_block)

    def highlight_block(self, text, block):
        raise NotImplementedError()

    def rehighlight(self):
        QApplication.setOverrideCursor(
            QCursor(Qt.WaitCursor))
        try:
            super().rehighlight()
        except RuntimeError:
            ...
        QApplication.restoreOverrideCursor()
