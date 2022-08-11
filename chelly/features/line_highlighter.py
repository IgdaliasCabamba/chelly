from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QColor, QTextFormat
from PySide6.QtCore import Qt
from ..core import Feature

class CaretLineHighLighter(Feature):
    def __init__(self, editor):
        super().__init__(editor)
        
        self.editor.cursorPositionChanged.connect(self.highlight_current_line)
        self.highlight_current_line()
    
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