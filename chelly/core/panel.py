from __future__ import annotations

from typing import TYPE_CHECKING, Any
from typing_extensions import Self

if TYPE_CHECKING:
    from ..api import ChellyEditor

from dataclasses import dataclass
from PySide6.QtWidgets import QFrame
import pprint

class Panel(QFrame):

    class Settings:
        __settings = dict()

        def __setattr__(self, __name: str, __value: Any) -> None:
            self.__settings[__name] = __value
        
        def __getattr__(self, __name: str) -> Any:
            return self.__settings.get(__name, False)
        
        def __delattr__(self, __name: str) -> None:
            self.__settings.pop(__name, None)
        
        def __repr__(self) -> str:
            return pprint.pformat(self.__settings)
        
        def __enter__(self) -> dict:
            return self.__settings
        
        def __exit__(self, *args, **kvargs) -> Self:
            return self
    
    @dataclass(frozen=True)
    class WidgetSettings:
        level:int = 0
        z_index:int = 0

    class Position(object):
        """
        Enumerates the possible panel positions
        """
        #: Top margin
        TOP = 0
        #: Left margin
        LEFT = 1
        #: Right margin
        RIGHT = 2
        #: Bottom margin
        BOTTOM = 3

        @classmethod
        def iterable(cls):
            """ Returns possible positions as an iterable (list) """
            return [cls.TOP, cls.LEFT, cls.RIGHT, cls.BOTTOM]


    def __init__(self, editor:ChellyEditor) -> None:
        super().__init__(editor)
        self.order_in_zone = -1
        self._scrollable = False
        self.__enabled = True
        self.__editor = editor
        self.editor.panels.refresh()
        self.setAutoFillBackground(False)
        self.__settings = Panel.Settings()
    
    @property
    def settings(self) -> Settings:
        return self.__settings

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, status:bool) -> None:
        self.__enabled = status
        
    @property
    def editor(self) -> ChellyEditor:
        return self.__editor
    
    @property
    def scrollable(self) -> bool:
        """
        A scrollable panel will follow the editor's scroll-bars. Left and right
        panels follow the vertical scrollbar. Top and bottom panels follow the
        horizontal scrollbar.
        :type: bool
        """
        return self._scrollable

    @scrollable.setter
    def scrollable(self, value:bool):
        self._scrollable = value
    
    def setVisible(self, visible:bool):
        """
        Shows/Hides the panel
        Automatically call CodeEdit.refresh_panels.
        :param visible: Visible state
        """
        super().setVisible(visible)
        if self.editor:
            self.editor.panels.refresh()
    
    @property
    def fixed_size_hint(self):
        return 0