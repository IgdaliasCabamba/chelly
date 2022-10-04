from __future__ import annotations

from typing import TYPE_CHECKING, Type, Union, Any
import pprint
from typing_extensions import Self

if TYPE_CHECKING:
    from ..api import ChellyEditor

class Feature(object):
    
    class Settings:

        __dict = dict()

        def __setattr__(self, __name: str, __value: Any) -> None:
            self.__dict[__name] = __value
        
        def __getattr__(self, __name: str) -> Any:
            return self.__dict.get(__name, False)
        
        def __delattr__(self, __name: str) -> None:
            self.__dict.pop(__name, None)
        
        def __repr__(self) -> str:
            return pprint.pformat(self.__dict)
        
        def __enter__(self) -> dict:
            return self.__dict
        
        def __exit__(self, *args, **kvargs) -> Self:
            return self
        
        @property
        def as_dict(self):
            return self.__dict

    def __init__(self, editor:ChellyEditor):
        self.__editor:object = editor
        self.__enabled = True
        self.__settings = Feature.Settings()
    
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
    
