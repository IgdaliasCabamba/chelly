from typing import Any, Dict, List, Optional, Union
from .chelly_property import chelly_property


class BaseElement:
    """The lowest level for editor elements"""

    def __init__(self, instance: Any) -> None:
        self._instance = instance

    @property
    def instance(self) -> Any:
        return self._instance

    def from_dict(self, element_properties_dict: Dict[str, Any]) -> None:
        for key, value in element_properties_dict.items():
            if hasattr(self, key):
                try:
                    setattr(self, key, value)
                except AttributeError:
                    pass

    def to_dict(self, excludes: list = None):
        if excludes is None:
            excludes = []

        res_dict = self.as_dict
        for exclude in excludes:
            if exclude in res_dict.keys():
                res_dict.pop(exclude, None)

    @property
    def as_dict(self) -> Dict[str, Any]:
        res = {}
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, chelly_property) and value not in {"as_dict"}:
                if chelly_property.is_shareable(value):
                    res[key] = value.fget(self)
        return res


__all__ = ["BaseElement"]
