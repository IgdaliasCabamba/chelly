import pathlib

from qtpy.QtCore import QFile, QIODevice, QObject, QSize, QSizeF, Qt, QUrl
from qtpy.QtGui import (QImage, QPyTextObject, QTextCharFormat, QTextCursor,
                        QTextDocument, QTextFormat, QTextFrameFormat,
                        QTextImageFormat, QTextObjectInterface)
from qtpy.QtSvg import QSvgRenderer
from qtpy.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                            QMessageBox, QPlainTextEdit, QPushButton,
                            QVBoxLayout, QWidget)

from ..core import Feature, TextEngine
from ..internal import ChellyFollowedValue, chelly_property

ANNOTATION_TEXT_FORMAT = QTextFormat.UserObject + 1
ANNOTATION_DATA = 1


class AnnotationTextCharFormat(QTextCharFormat):
    def __init__(self, parent=None):
        super().__init__()


class AnnotationTextObject(QPyTextObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def intrinsicSize(self, doc, posInDocument, format):
        text_obj_data = format.property(ANNOTATION_DATA)

        if isinstance(text_obj_data, dict):
            return QSizeF(text_obj_data["data"]["width"], text_obj_data["data"]["height"])

        return QSizeF(50, 50)

    def drawObject(self, painter, rect, doc, posInDocument, format):
        pass


class RichAnnotation(QWidget):
    def __init__(self, editor, id_: str, line: int):
        super().__init__()
        self._editor = editor
        self.setup_text_object()

        self.id_ = id_
        self._line = line

    def setup_text_object(self) -> None:
        annotation_interface = AnnotationTextObject(self)
        doc_layout = self._editor.document().documentLayout()
        doc_layout.registerHandler(
            ANNOTATION_TEXT_FORMAT, annotation_interface)

    def display(self, width: int, height: int) -> dict:
        annotation_char_format = AnnotationTextCharFormat()
        annotation_char_format.setObjectType(ANNOTATION_TEXT_FORMAT)
        annotation_char_format.setProperty(
            ANNOTATION_DATA,
            {
                "id": self.id_,
                "data": {
                    "width": width,
                    "height": height
                }
            })

        cursor = self._editor.textCursor()
        cursor.insertText(chr(0xfffc), annotation_char_format)
        self._editor.setTextCursor(cursor)

        return {
            "block_number": cursor.blockNumber(),
            "char_format": annotation_char_format
        }
    
    def destroy(self):
        ...


class RichAnnotations(Feature):
    
    def __init__(self, editor):
        super().__init__(editor)
        self.__annotation_lines = list()
        self.__annotations_data = dict()
        
        #self.__annotation_lines.append(cursor.blockNumber())
    
    def append(self, id_: str, width: int, height: int, line: int) -> RichAnnotation:
        x = RichAnnotation(self.editor, id_, line)
        x.display(width, height)
        self.__annotation_lines.append(x)
        return x
    
    def remove(self, id_: str = None, line: int = None) -> RichAnnotation:
        ...
    
    def get(self, id_: str = None, line: int = None) -> RichAnnotation:
        ...