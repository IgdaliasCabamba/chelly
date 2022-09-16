from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

if TYPE_CHECKING:
    from ..api import ChellyEditor

class Manager(QObject):
    
    on_state_changed = Signal(object)

    def __init__(self, editor:ChellyEditor):
        super().__init__()
        self.__editor = editor
    
    @property
    def editor(self):
        return self.__editor
    
