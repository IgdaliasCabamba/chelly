import inspect
from types import NoneType, UnionType
from typing import Any, Iterable, List, Optional, Type, Union

import typing_extensions
from typing_extensions import Self

from .chelly_follow import ChellyFollowedValue
from functools import lru_cache
from nemoize import memoize


class chelly_property:
    """
    Chelly property is a shareable object among chelly components
    """

    @staticmethod
    def get_signature(klass: Any, c_property_name: str) -> Optional[inspect.Signature]:
        c_property = getattr(klass.__class__, c_property_name, None)

        if c_property is None:
            return None

        return inspect.signature(c_property.fget)

    @staticmethod
    @memoize(arg_hash_function=str, max_size=16)
    def check_types(required_types: Iterable, given_type: Type) -> bool:
        class_name = getattr(given_type, "__name__", None)

        if class_name is None:
            return True

        for _type in [
            "Any",
            "None",
            "NoneType",
            "Optional",
            Any,
            None,
            NoneType,
            Optional,
        ]:
            if _type in required_types:
                return True

        for required_type in required_types:
            if required_type == class_name or required_type == given_type:
                return True

        return False

    @staticmethod
    def get_functions_arg_types(*functions) -> List[Type]:
        res = []

        for function in functions:
            type_hints = typing_extensions.get_type_hints(function)

            for param, type_hint in type_hints.items():
                if param == "return":
                    continue

                if typing_extensions.get_origin(type_hint) in {UnionType, Union}:
                    for arg in typing_extensions.get_args(type_hint):
                        res.append(arg)
                else:
                    res.append(type_hint)

        return res

    __slots__ = ("fget", "fset", "fdel", "ffollow", "_doc", "typed", "args", "kwargs")

    def __init__(
        self, fget=None, fset=None, fdel=None, ffollow=None, doc=None, *args, **kwargs
    ) -> None:
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.ffollow = ffollow
        if doc is None and fget is not None:
            doc = fget.__doc__
        self._doc = doc
        self.typed: Type = Any
        self.kwargs = kwargs
        self.args = args

        if "typed" in kwargs.keys():
            self.typed = kwargs["typed"]

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

        if self.typed:
            given_type = type(value)

            if isinstance(value, ChellyFollowedValue):
                given_type = type(value.value)

            required_types: tuple = self.get_functions_arg_types(self.fset)

            if not self.check_types(required_types, given_type):
                raise TypeError(f"Expected {required_types}. Got: {given_type}")

        if isinstance(value, ChellyFollowedValue):
            self.fset(obj, value.value)

        else:
            self.fset(obj, value)

            if self.ffollow is not None:
                self.ffollow(self=obj, origin=obj, value=value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("Can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(
            fget,
            self.fset,
            self.fdel,
            self.ffollow,
            self._doc,
            *self.args,
            **self.kwargs,
        )

    def setter(self, fset):
        return type(self)(
            self.fget,
            fset,
            self.fdel,
            self.ffollow,
            self._doc,
            *self.args,
            **self.kwargs,
        )

    def deleter(self, fdel):
        return type(self)(
            self.fget,
            self.fset,
            fdel,
            self.ffollow,
            self._doc,
            *self.args,
            **self.kwargs,
        )

    def follower(self, ffollow):
        return type(self)(
            self.fget,
            self.fset,
            self.fdel,
            ffollow,
            self._doc,
            *self.args,
            **self.kwargs,
        )


if __name__ == "__main__":

    class Test:
        def __init__(self, val: int = 0, val1: str = "chelly"):
            self._val: int = val
            self._val1: str = val1

        @chelly_property
        def val(self) -> int:
            return self._val

        @val.setter
        def val(self, new_value: int) -> None:
            self._val = new_value

        @val.deleter
        def val(self) -> None:
            self._val = None

        def __set_val1(self, new_value: str) -> None:  # Write only
            self._val1 = new_value
            assert self._val1 == new_value

        val1 = chelly_property(fset=__set_val1, typed=True)
        del __set_val1

    test = Test(18)
    assert test.val == 18

    res = test.val = 13
    assert res == 13
    assert test.val == 13

    del test.val
    assert test.val is None

    test.val1 = "Icode"


__all__ = ["Test", "chelly_property", "res", "test"]
