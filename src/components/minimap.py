import PySide6
from PySide6.QtCore import Signal, Qt, QSize, QRect
from PySide6.QtGui import QColor, QTextCursor, QFont, QPainter, QTextBlock
from PySide6.QtWidgets import QPlainTextEdit, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from ..managers import FeaturesManager, LanguagesManager
from ..core import Properties, LexerExceptions, PropertiesExceptions, FeaturesExceptions, Panel

class MiniChellyMap(Panel):
    def __init__(self, editor):
        super().__init__(editor)

        self.amount_of_blocks = self.editor.blockCount()

        a = QGraphicsDropShadowEffect(self)
        a.setColor(QColor("#111111"))
        a.setXOffset(-3)
        a.setYOffset(1)
        a.setBlurRadius(6)
        self.setGraphicsEffect(a)

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0,0,0,0)

        self._minimap = QPlainTextEdit(self)
        self._minimap.zoomOut(5)
        self._minimap.setReadOnly(True)
        self._minimap.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._minimap.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.box.addWidget(self._minimap)
        self.setLayout(self.box)

        self.editor.document().contentsChange.connect(self.update_minimap)
    
    def move_cursor_to(self, line):
        cursor = self._minimap.textCursor()
        block = self._minimap.document().findBlockByLineNumber(line)
        cursor.setPosition(block.position())
        #print(block.position())
        #print(self.editor.document().findBlockByLineNumber(line).position())
    
    def line_text(self, line_nbr) -> str:
        if line_nbr is None:
            return ''
        doc = self.editor.document()
        block = doc.findBlockByLineNumber(line_nbr)
        return block.text()

    def update_minimap(self, pos, charsrem, charsadd):
        self.move_cursor_to(self.editor.textCursor().blockNumber())
        editor = self._minimap
        text_cursor = editor.textCursor()
        
        for x in range(charsrem):
            text_cursor.deletePreviousChar()

        if charsadd:
            if self.amount_of_blocks == self.editor.blockCount():
                text = self.line_text(self.editor.textCursor().blockNumber())
                cur_pos = self.editor.textCursor().columnNumber()
                if charsadd > 1:
                    value = text[cur_pos-charsadd:cur_pos]
                    print(value)
                    text_cursor.insertText(value)
                else:
                    text_cursor.insertText(text[cur_pos-charsadd])
            else:
                t = self.editor.document().toPlainText()
                self._minimap.document().setPlainText(t)

        self.amount_of_blocks = self.editor.blockCount()
        editor.setTextCursor(text_cursor)

    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the right, we only need
        to compute the width
        """
        return QSize(200, 0)