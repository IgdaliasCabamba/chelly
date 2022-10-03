from ..core import Manager, ChellyStyle
from qtpy.QtGui import QPalette, QColor
from ..core import ChellyStyle

class ChellyStyleManager(Manager):
    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.__qpalette = QPalette()
        self.__theme = ChellyStyle(editor)
    
    def __enter__(self):
        return self.__theme
    
    def __exit__(self, *args, **kvargs):
        return self
    
    @property
    def qpalette(self) -> QPalette:
        return self.__qpalette
    
    @property
    def theme(self) -> ChellyStyle:
        return self.__theme
    
    @theme.setter
    def theme(self, new_theme:ChellyStyle) -> None:
        if callable(new_theme):
            theme = new_theme(self.editor)
        else:
            new_theme.add_editor(self.editor)
            theme = new_theme

        self.__theme = theme

