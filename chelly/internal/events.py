from typing import Any, Tuple, Type
from typing_extensions import Self

class ChellyEvent:
    
    class TypeError(Exception):
        ...

    def __init__(self, *emit_types:Tuple[Type]) -> None:
        self.__emit_types = emit_types
        self.__event_handlers = []
    
    def connect(self, callable_object:object) -> Self:
        if callable(callable_object):
            self.__event_handlers.append(callable_object)
        return self
    
    def disconnect(self, callable_object:object) -> Self:
        if callable_object in self.__event_handlers:
            self.__event_handlers.remove(callable_object)
        return self
    
    def emit(self, *callable_objects:Tuple[Any]) -> Self:
        for i in range(len(callable_objects)):
            if self.__emit_types[i] is not Any:
                if not isinstance(callable_objects[i], self.__emit_types[i]):
                    raise ChellyEvent.TypeError(f"Expected: {self.__emit_types[i]}, Got: {type(callable_objects[i])}")

        for handler in self.__event_handlers:
            handler(*callable_objects)
        
        return self
