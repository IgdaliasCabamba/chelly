from inspect import signature
from typing import Any, Type, Union, Optional
from typing_extensions import Self, get_origin, get_args, types
from types import UnionType, NoneType

from types import FunctionType

class ChellyShareable:
    ...

class chelly_property:
    """
    Chelly property is a shareable object among chelly components
    """
    @staticmethod
    def is_shareable(klass: Any, c_property_name: str) -> Optional[bool]:
        c_property = getattr(klass.__class__, c_property_name, None)
        if c_property is None:
            return None

        method_sig = signature(c_property.fget)
        if method_sig.return_annotation is ChellyShareable:
            return True

        return False

    __slots__ = ("fget","fset","fdel", "_doc", "value_type", "args", "kwargs")

    def __init__(self, fget=None, fset=None, fdel=None, doc=None, *args, **kwargs) -> None:
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self._doc = doc
        self.value_type: Type = Any
        self.kwargs = kwargs
        self.args = args

        if "value_type" in kwargs.keys():
            self.value_type = kwargs["value_type"]
    
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
        
        if self.value_type not in {Any, None, NoneType}:
            if get_origin(self.value_type) in (UnionType, Union):
                if type(value) not in get_args(self.value_type):
                    raise TypeError(f"Expected {self.value_type}. Got: {type(value)}")

        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("Can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self._doc, *self.args, **self.kwargs)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self._doc, *self.args, **self.kwargs)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self._doc, *self.args, **self.kwargs)

if __name__ == "__main__":
    
    class Test:
        def __init__(self, val:int = 0, val1: str = "chelly"):
            self._val: int = val
            self._val1: str = val1

        # python >= 3.10: @chelly_property(value_type=int|str|float)
        # python >= 3.7:
        @chelly_property(value_type=Union[int,str,float])
        def val(self) -> ChellyShareable:
            return self._val
        
        @val.setter
        def val(self, new_value:int) -> None:
            self._val = new_value
        
        @val.deleter
        def val(self) -> None:
            self._val = None
        
        def __set_val1(self, new_value:str) -> None: #Write only
            self._val1 = new_value
            assert self._val1 == new_value
        
        val1 = chelly_property(fset=__set_val1, value_type=str)
        del __set_val1
    
    test = Test(18)
    assert chelly_property.is_shareable(test, "val")
    assert test.val == 18
    
    res = test.val = 13
    assert res == 13
    assert test.val == 13
    
    del test.val
    assert test.val is None

    test.val1 = "Icode"