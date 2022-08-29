from typing import Any
import pprint
from typing_extensions import Self

class Feature(object):
    
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

    def __init__(self, editor):
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
    def editor(self) -> object:
        return self.__editor
    
