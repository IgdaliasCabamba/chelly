from __future__ import annotations

from typing import TYPE_CHECKING, Type, Union, Any, Dict, List

if TYPE_CHECKING:
    from ..api import ChellyEditor

from string import Template
from typing import Any

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QPalette
from typing_extensions import Self
from ..utils.helpers import ChellyEvent

class ChellyTheme:
    _selection_background = QColor(Qt.GlobalColor.darkBlue)
    _selection_background.setAlpha(180)
    
    main = {
        "selection":{
            "background": _selection_background,
            "foreground":QColor(Qt.GlobalColor.white)
        }
    }