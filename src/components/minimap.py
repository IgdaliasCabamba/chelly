import PySide6
from PySide6.QtCore import Signal, Qt, QSize, QRect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPlainTextEdit, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from ..managers import FeaturesManager, LanguagesManager
from ..core import Properties, LexerExceptions, PropertiesExceptions, FeaturesExceptions, Panel

class MiniChellyMap(Panel):
    def __init__(self, editor):
        super().__init__(editor)

        a = QGraphicsDropShadowEffect(self)
        a.setColor(QColor("#111111"))
        a.setXOffset(-3)
        a.setYOffset(1)
        a.setBlurRadius(6)
        self.setGraphicsEffect(a)

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0,0,0,0)

        self._minimap = QPlainTextEdit(self)
        self._minimap.setDocument(self.editor.document())
        self._minimap.setReadOnly(True)
        self._minimap.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._minimap.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.box.addWidget(self._minimap)
        self.setLayout(self.box)
    
    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the right, we only need
        to compute the width
        """
        return QSize(200, 0)