from __future__ import annotations

from typing import TYPE_CHECKING, Any, List
from .chelly_cache import ChellyCache
from .__base__ import BaseElement

if TYPE_CHECKING:
    from ..api import ChellyEditor

class Feature(object):
    
    class _Properties(BaseElement):
        
        @property
        def feature(self) -> Feature:
            return self.instance
    
    class _Styles(BaseElement):
        
        @property
        def feature(self) -> Feature:
            return self.instance
            
    @property
    def properties(self) -> _Properties:
        return self.__properties
    
    @property
    def styles(self) -> _Styles:
        return self.__styles
    
    def __init__(self, editor:ChellyEditor):
        self.__editor:object = editor
        self.__enabled = True
        self.__properties = Feature._Properties(self)
        self.__styles = Feature._Styles(self)

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, status:bool) -> None:
        self.__enabled = status

    @property
    def editor(self) -> ChellyEditor:
        return self.__editor