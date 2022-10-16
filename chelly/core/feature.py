from __future__ import annotations

from typing import TYPE_CHECKING, Type, Union, Any
from dataclasses import dataclass
from .chelly_cache import ChellyCache

if TYPE_CHECKING:
    from ..api import ChellyEditor

class Feature(object):
    
    @dataclass(frozen=True)
    class Defaults:
        ...
    
    class _Properties:
        def __init__(self, feature_instance:Feature) -> None:
            self._feature_instance = feature_instance
        
        @property
        def feature(self):
            return self._feature_instance
            
    
    def __init__(self, editor:ChellyEditor):
        self.__editor:object = editor
        self.__enabled = True
        self.__cache = ChellyCache()
        self.__properties = Feature._Properties(self)
    
    @property
    def properties(self) -> _Properties:
        return self.__properties
    
    @property
    def cache(self) -> ChellyCache:
        return self.__cache

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, status:bool) -> None:
        self.__enabled = status

    @property
    def editor(self) -> ChellyEditor:
        return self.__editor
    
