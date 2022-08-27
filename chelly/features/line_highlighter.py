from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QColor, QTextFormat, QBrush
from PySide6.QtCore import Qt
from ..core import Feature, TextDecoration, drift_color

class CaretLineHighLighter(Feature):
    @property
    def background(self):
        """
        Background color of the caret line. Default is to use a color slightly
        darker/lighter than the background color. You can override the
        automatic color by setting up this property
        """
        if self._color or not self.editor:
            return self._color
        else:
            return drift_color(self._color, 110)

    @background.setter
    def background(self, value):
        self._color = value
        self.refresh()

    def __init__(self, editor):
        super().__init__(editor)
        self._decoration = None
        self._pos = -1
        self._color = QColor(Qt.GlobalColor.yellow).lighter(160)
        
        self.editor.cursorPositionChanged.connect(self.refresh)
        #self.editor.new_text_set.connect(self.refresh)
        self.refresh()
    
    def _clear_deco(self):
        """ Clear line decoration """
        if self._decoration:
            self.editor.decorations.remove(self._decoration)
            self._decoration = None

    def refresh(self):
        """
        Updates the current line decoration
        """
        self._clear_deco()
        if self._color:
            color = self._color
        brush = QBrush(color)
        self._decoration = TextDecoration(self.editor.textCursor())
        self._decoration.set_background(brush)
        self._decoration.set_full_width()
        self._decoration.set_foreground(QColor("#fff"))
        self.editor.decorations.append(self._decoration)

    def highlight_current_line(self):
        extra_selections = []

        if not self.editor.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor(Qt.GlobalColor.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setForeground(QColor("#fff"))

            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)

            selection.cursor = self.editor.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.editor.setExtraSelections(extra_selections)