from enum import Enum


class Character(Enum):
    SPACE: str = " "
    TAB: str = "\t"
    EMPTY: str = str()
    LARGEST = "W"


__all__ = ["Character"]
