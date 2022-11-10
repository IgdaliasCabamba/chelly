from inspect import signature, Signature
from typing import Any, Type, Union, Optional, Type
from typing_extensions import Self, get_origin, get_args, types
from types import UnionType, NoneType

from types import FunctionType
import abc

class ChellyFollowable(metaclass=abc.ABCMeta):
    def __init__(self, editor):
        self.__editor = editor

    @property
    def editor(self):
        return self.__editor
    
    
    def imitate(self, other:Self):
        ...
        # TODO:

class ChellyTracked:
    
    @property
    def value(self) -> Any:
        return self.__value

    def __init__(self, value):
        self.__value = value
    
    def __call__(self, *args, **kwargs):
        ...
    

class chelly_imitable:

    def __init__(self, fget=None, fset=None, fdel=None, ftrack=None, doc=None) -> None:
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.ftrack = ftrack
        if doc is None and fget is not None:
            doc = fget.__doc__
        self._doc = doc
    
    def __call__(self, *args, **kwargs) -> Self:
        if args and self.fget is None:
            self.fget = args[0]
        return self

    def __get__(self, obj, objtype=None, *args, **kwargs) -> Any:
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("Unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value) -> None:
        if self.fset is None:
            raise AttributeError("Can't set attribute")
        
        if isinstance(value, ChellyTracked):
            self.fset(obj, value.value)
            return None
        
        self.fset(obj, value)

        if self.ftrack is not None:
            self.ftrack(self=obj, origin=obj, value=value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("Can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.ftrack, self._doc)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.ftrack, self._doc)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.ftrack, self._doc)
    
    def tracker(self, ftrack):
        return type(self)(self.fget, self.fset, self.fdel, ftrack, self._doc)

    
# in order to avoid recursion, block the setter.
# this way any other follower can set the value recursively
# while the origin setter is setting the origin value
