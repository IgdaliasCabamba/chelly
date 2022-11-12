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
    
    
    @abc.abstractmethod
    def imitate(self, other:Self):
        ...
        # TODO:

class ChellyFollowedValue:
    
    @property
    def value(self) -> Any:
        return self.__value

    def __init__(self, value):
        self.__value = value
    
    def __call__(self, *args, **kwargs):
        ...