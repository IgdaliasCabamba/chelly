import PySide6
from PySide6.QtCore import Signal, Qt, QSize, QRect
from PySide6.QtGui import QColor, QTextCursor, QFont, QPainter, QTextBlock
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
        self._minimap.zoomOut(5)
        self._minimap.setReadOnly(True)
        self._minimap.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._minimap.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.box.addWidget(self._minimap)
        self.setLayout(self.box)

        self.editor.document().contentsChange.connect(self.update_minimap)
    
    def move_cursor_to(self, line):
        cursor = self._minimap.textCursor()
        block = self._minimap.document().findBlockByNumber(line)
        cursor.setPosition(block.position())
    
    def line_text(self, line_nbr):
        """
        Gets the text of the specified line
        :param line_nbr: The line number of the text to get
        :return: Entire line's text
        :rtype: str
        """

        # Under some (apparent) race conditions, this function can be called
        # with a None line number. This should be fixed in a better way, but
        # for now we return an empty string to avoid crashes.
        if line_nbr is None:
            return ''
        doc = self.editor.document()
        block = doc.findBlock(line_nbr)
        #print(line_nbr)
        return block.text()

    def update_minimap(self, pos, charsrem, charsadd):
        #t = self.editor.document().toPlainText()
        #self._minimap.document().setPlainText(t)
        self.move_cursor_to(self.editor.textCursor().blockNumber())
        editor = self._minimap
        text_cursor = editor.textCursor()
        
        for x in range(charsrem):
            text_cursor.deletePreviousChar()
        
        if charsadd:
            text = self.line_text(pos)
            if charsadd > 1:
                pass
            else:
                text_cursor.insertText(text[-1])
        
        editor.setTextCursor(text_cursor)

    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the right, we only need
        to compute the width
        """
        return QSize(200, 0)