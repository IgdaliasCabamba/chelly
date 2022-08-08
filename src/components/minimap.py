import PySide6
from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import (QColor, QFont, QFontMetrics, QPainter, QTextBlock,
                           QTextCursor, QTextOption)
from PySide6.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout,
                               QPlainTextEdit, QScrollBar, QVBoxLayout)
from .code_editor import CodeEditor
from .scrollbar import SliderArea

from ..core import (FeaturesExceptions, LexerExceptions, Panel, Properties,
                    PropertiesExceptions, TextFunctions)
from ..managers import FeaturesManager, LanguagesManager

class MiniMap(CodeEditor):
    def __init__(self, parent):
        super().__init__(parent)

        self.editor = parent.editor
        self._amount_of_blocks = TextFunctions(self.editor).line_count
        self.current_scroll_value = self.editor.verticalScrollBar().value()
        
        self.slider = SliderArea(self)
        self.slider.show()

        self.setMouseTracking(True)
        self.setTabStopDistance(QFontMetrics(
            self.font()).horizontalAdvance(' ') * 2)

        self.zoomOut(8)
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.editor.document().contentsChange.connect(self.update_contents)
        self.editor.on_painted.connect(self.update_ui)
    
    def update_ui(self):
        print("AAAA")
        self.scroll_map()
    
    def update_contents(self, pos, charsrem, charsadd):
        line_number = TextFunctions(self.editor).current_line_nbr
        TextFunctions(self).move_cursor_to_line(line_number)
        text = TextFunctions(self.editor).text_at_line(line_number)

        if self._amount_of_blocks == TextFunctions(self.editor).line_count:
            TextFunctions(self).set_text_at_line(
                self.textCursor().blockNumber(), text)
            TextFunctions(self).move_cursor_to_line(line_number)
        else:
            self.document().setPlainText(
                self.editor.document().toPlainText()
            )
            TextFunctions(self).move_cursor_to_line(
                TextFunctions(self.editor).current_line_nbr
            )

        self._amount_of_blocks = TextFunctions(self.editor).line_count
    
    def scroll_map(self):
        first_visible_line = self.editor.firstVisibleBlock().firstLineNumber()
        
        num_doc_lines = self.editor.document().lineCount()

        #num_visible_lines = self.editor.SendScintilla(
        #    QsciScintilla.SCI_DOCLINEFROMVISIBLE, num_doc_lines
        #)
        num_visible_lines = TextFunctions(self.editor).visible_lines

        lines_on_screen = TextFunctions(self.editor).visible_lines

        if num_visible_lines > lines_on_screen:
            last_top_visible_line = num_visible_lines - lines_on_screen

            #num_map_visible_lines = self.SendScintilla(
            #    QsciScintilla.SCI_DOCLINEFROMVISIBLE, num_doc_lines
            #)
            num_map_visible_lines = TextFunctions(self).visible_lines

            lines_on_screenm = TextFunctions(self).visible_lines

            last_top_visible_linem = num_map_visible_lines - lines_on_screenm

            portion = first_visible_line / last_top_visible_line

            first_visible_linem = round(last_top_visible_linem * portion)

            self.verticalScrollBar().setValue(first_visible_linem)

            line_nr = TextFunctions(self.editor).get_line_nbr_from_position(0,0)
            higher_pos = TextFunctions(self.editor).get_line_pos_from_number(line_nr)

            y = higher_pos   
            #y = self.SendScintilla(QsciScintilla.SCI_POINTYFROMPOSITION, 0, higher_pos)

            self.slider.move(0, y)

        self.current_scroll_value = self.editor.verticalScrollBar().value()

    def scroll_area(self, pos_parent, line_area):
        line = TextFunctions(self).get_line_nbr_from_position(pos_parent.x(), pos_parent.y())
        self.editor.verticalScrollBar().setValue(line - line_area)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        line = TextFunctions(self).get_line_nbr_from_position(event.pos().x(), event.pos().y())
        TextFunctions(self.editor).move_cursor_to_line(line)

        los = TextFunctions(self.editor).visible_lines / 2
        scroll_value = self.editor.verticalScrollBar().value()

        if self.current_scroll_value < scroll_value:
            self.editor.verticalScrollBar().setValue(scroll_value + los)
        else:
            self.editor.verticalScrollBar().setValue(scroll_value - los)
    
    def wheelEvent(self, event):
        super().wheelEvent(event)
        self.editor.wheelEvent(event)

class MiniChellyMap(Panel):
    def __init__(self, editor):
        super().__init__(editor)

        drop_shadow = QGraphicsDropShadowEffect(self)
        drop_shadow.setColor(QColor("#111111"))
        drop_shadow.setXOffset(-3)
        drop_shadow.setYOffset(1)
        drop_shadow.setBlurRadius(6)
        self.setGraphicsEffect(drop_shadow)

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._minimap = MiniMap(self)

        self.box.addWidget(self._minimap)
        self.setLayout(self.box)

    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the right, we only need
        to compute the width
        """
        return QSize(140, 0)
