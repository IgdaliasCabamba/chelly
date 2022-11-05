from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api import ChellyEditor

from ..core import Manager
from qtpy.QtGui import QPalette, QColor
from ..core import ChellyTheme
from typing_extensions import Self

class ChellyStyleManager(Manager):
    def __init__(self, editor) -> None:
        super().__init__(editor)

        self.__palette = editor.palette()
        self.__theme = ChellyTheme(self.__palette)
        self.__theme.on_palette_changed.connect(self.update_palette)
    
    def __enter__(self) -> ChellyTheme:
        return self.__theme
    
    def __exit__(self, *args, **kvargs):
        return self
    
    @property
    def palette(self) -> ChellyPalette:
        return self.__palette
    
    @property
    def theme(self) -> ChellyTheme:
        return self.__theme
    
    @theme.setter
    def theme(self, new_theme: ChellyTheme) -> None:
        if callable(new_theme):
            theme = new_theme()
        else:
            theme = new_theme
        
        theme.on_palette_changed.connect(self.update_palette)

        self.__theme = theme
    
    def update_palette(self, *args, **kargs) -> None:
        self.__palette.setColor(*args, **kargs)
        self.editor.setPalette(self.__palette)
    
    def __shared_reference(self, other_manager:Self) -> Self:
        from_theme = other_manager.theme
        self.theme = from_theme
        
    shared_reference = property(fset=__shared_reference)
    del __shared_reference