from PySide6.QtWidgets import QTextEdit, QPlainTextEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QTextFormat
from .margins import LineNumberMargin

class GenericCodeEditor(QPlainTextEdit):
    
    on_resized = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.highlight_current_line()
        self.number_bar = LineNumberMargin(self)
    
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.on_resized.emit()

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor(Qt.GlobalColor.yellow).lighter(160)
            selection.format.setBackground(line_color)

            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)