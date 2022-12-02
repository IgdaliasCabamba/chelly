from ..core import Feature, TextEngine
from ..internal import chelly_property, ChellyFollowedValue
from qtpy.QtGui import QTextCursor, QTextDocument, QTextFrameFormat

class RichAnnotation(Feature):
    def __init__(self, editor):
        super().__init__(editor)
        self.__annotations = []
    
    def append(self, text:str):
        ...