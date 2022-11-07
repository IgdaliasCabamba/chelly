from __future__ import annotations

from typing import TYPE_CHECKING, Any, List
from typing_extensions import Self

if TYPE_CHECKING:
    from ...api import ChellyEditor

from dataclasses import dataclass
from qtpy.QtWidgets import QFrame
from ...internal import BaseElement

class Panel(QFrame):
    
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

    class _Properties(BaseElement):
        
        @property
        def panel(self) -> Panel:
            return self.instance
    
    class _Styles(BaseElement):
        
        @property
        def panel(self) -> Panel:
            return self.instance
    
    @property
    def properties(self) -> _Properties:
        return self.__properties
    
    @property
    def styles(self) -> _Styles:
        return self.__styles

    def __init__(self, editor:ChellyEditor) -> None:
        super().__init__(editor)
        self.order_in_zone = -1
        self._scrollable = False
        self.__enabled = True
        self.__editor = editor
        self.editor.panels.refresh()
        self.setAutoFillBackground(False)
        self.__properties = Panel._Properties(self)
        self.__styles = Panel._Styles(self)

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
    
    @property
    def shared_reference(self) -> dict:
        return {
            "styles":self.styles,
            "properties":self.properties
        }

    @shared_reference.setter
    def shared_reference(self, panel_data:dict = None) -> None:
        for key, value in panel_data.items():
            if hasattr(self, key):
                try:
                    setattr(self, key, value)
                except AttributeError:
                    pass