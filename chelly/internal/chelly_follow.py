from inspect import signature, Signature
from typing import Any, Type, Union, Optional, Type
from typing_extensions import Self, get_origin, get_args, types
from types import UnionType, NoneType

from types import FunctionType
import abc


class ChellyFollowable(metaclass=abc.ABCMeta):
    class NonFolloableValue:
        ...

    def __init__(self, editor):
        self.__editor = editor

    @property
    def editor(self):
        return self.__editor

    @abc.abstractmethod
    def follow(self, other: Self):
        ...


class ChellyFollowedValue:
    @property
    def value(self) -> Any:
        return self.__value

    def __init__(self, value):
        self.__value = value

    def __call__(self, *args, **kwargs) -> Any:
        new_value = kwargs.get("value", ChellyFollowable.NonFolloableValue)

        if new_value is ChellyFollowable.NonFolloableValue:
            return self.__value

        self.__value = new_value

    def __enter__(self) -> Any:
        return self.__value

    def __exit__(self, *args, **kwargs) -> Any:
        return self


__all__ = ["ChellyFollowable", "ChellyFollowedValue"]
