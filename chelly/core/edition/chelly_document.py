from typing import List
from typing_extensions import Self
from ..utils import TextEngine, Character
from ...internal import ChellyEvent
from qtpy.QtWidgets import QPlainTextEdit


class ChellyDocument:
    @property
    def editor(self) -> QPlainTextEdit:
        return self._editor

    def __init__(self, editor: QPlainTextEdit):
        self.on_contents_changed = ChellyEvent(object, int, int, int)

        self._editor = editor
        self._editor.document().contentsChange.connect(self.__update_contents)

    def __update_contents(
        self, from_: int = 0, charsremoved: int = 0, charsadded: int = 0
    ):
        self.on_contents_changed.emit(self._editor, from_, charsremoved, charsadded)


__all__ = ["ChellyDocument"]
