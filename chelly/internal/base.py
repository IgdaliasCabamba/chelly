from typing import Any, Dict, List, Optional, Union

class BaseElement:
    """The lowest level for editor elements"""

    def __init__(self, instance: Any) -> None:
        self._instance = instance
    
    @property
    def instance(self) -> Any:
        return self._instance

    @property
    def as_dict(self) -> Dict[str, Any]:
        res = {}
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, property) and value not in {"as_dict"}:
                res[key] = value.fget(self)

        return res
