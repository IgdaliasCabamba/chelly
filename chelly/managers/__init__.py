"""Implement a set of classes to help the ChellyEditor to handle the components and features.

This module allows the ChellyEditor to manage features, lexers, and panels.

Modules exported by this package:

- `features`: Provide the functionalities to extend and manage the editor functionalities.
- `langauges`: Provide the functionalities to manage the editor lexer.
- `widgets`: Provide the functionalities to manage the editor panels.
"""

from .features import FeaturesManager
from .languages import LanguagesManager
from .widgets import PanelsManager