from __future__ import annotations

from typing import TYPE_CHECKING, Any, List
from ..chelly_cache import ChellyCache
from ...internal import BaseElement

if TYPE_CHECKING:
    from ...api import ChellyEditor

class Feature(object):
    
    class _Properties(BaseElement):
        
        @property
        def feature(self) -> Feature:
            return self.instance
            
    @property
    def properties(self) -> _Properties:
        return self.__properties
    
    def __init__(self, editor:ChellyEditor):
        self.__editor:object = editor
        self.__enabled = True
        self.__properties = Feature._Properties(self)

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
    def shared_reference(self) -> dict:
        return {"properties":self.properties}

    @shared_reference.setter
    def shared_reference(self, feature_data:dict) -> None:
        for key, value in feature_data.items():
            if hasattr(self, key):
                try:
                    setattr(self, key, value)
                except AttributeError:
                    pass