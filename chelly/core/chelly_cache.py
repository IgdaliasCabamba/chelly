import pprint
from types import LambdaType
from typing import Any, Callable
from typing_extensions import Self


class ChellyCache:
    def __init__(
        self, inital_value: Any, default: Any = None, update_source: LambdaType = None
    ) -> None:
        self.value = inital_value
        self.default = default
        self.update_source = update_source

    @property
    def changed(self) -> bool:
        updated_value = self.update_source()

        if self.value == updated_value:
            return False

        self.value = updated_value

        return True

    def __repr__(self) -> str:
        return pprint.pformat(self.value)

    def __enter__(self) -> dict:
        return self.value

    def __exit__(self, *args, **kvargs) -> Self:
        return self


__all__ = ["ChellyCache"]
