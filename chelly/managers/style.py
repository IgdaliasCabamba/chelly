from ..core import Manager, ChellyStyle
from PySide6.QtGui import QPalette, QColor

class ChellyStyleManager(Manager):
    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.__qpalette = QPalette()
        self.__theme = None
    
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
            theme = new_theme

        self.__theme = theme

