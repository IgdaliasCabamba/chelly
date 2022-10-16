import pprint
from typing import Any
from typing_extensions import Self

class ChellyCache:

    class NoneAttr:
        ...

    # TODO transform this in cache

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__[__name] = __value
    
    def __getattr__(self, __name: str) -> Any:
        attr = self.__dict__.get(__name, ChellyCache.NoneAttr)
        return None
    
    def __delattr__(self, __name: str) -> None:
        self.__dict__.pop(__name, None)
    
    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
    
    def __enter__(self) -> dict:
        return self.__dict__
    
    def __exit__(self, *args, **kvargs) -> Self:
        return self
    
    def clear_all(self):
        print(self.__dict__)
    
    def has(self, __name:str) -> bool:
        return bool(__name in self.__dict__.keys())
    
    @property
    def as_dict(self):
        return self.__dict__
