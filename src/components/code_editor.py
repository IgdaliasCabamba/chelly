from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QTextEdit
from PyQt6.QtGui import QColor, QTextFormat
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from .breadcrumbs import Breadcrumb
from .margins import LineNumberMargin
from .generic_editor import GenericCodeEditor
import pprint

class ChellyEditor(QPlainTextEdit):
    
    on_resized = pyqtSignal()
    on_painted = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.highlight_current_line()
        self.number_bar = LineNumberMargin(self)
        self._visible_blocks = list()
    
    @property
    def visible_blocks(self):
        """
        Returns the list of visible blocks.
        Each element in the list is a tuple made up of the line top position,
        the line number and the QTextBlock itself.
        :return: A list of tuple(top_position, line_number, block)
        :rtype: List of tuple(int, int, QtWidgets.QTextBlock)
        """
        return self._visible_blocks
    
    def paintEvent(self, event):
        """
        Overrides paint event to update the list of visible blocks and emit
        the painted event.
        :param e: paint event
        """
        self._update_visible_blocks(event)
        super().paintEvent(event)
        self.on_painted.emit(event)
    
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

    def _update_visible_blocks(self, *args) -> None:
        """ Updates the list of visible blocks """
        self._visible_blocks[:] = []
        block = self.firstVisibleBlock()
        block_nbr = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(
            self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        ebottom_top = 0
        ebottom_bottom = self.height()
        first_block = True
        while block.isValid():
            visible = (top >= ebottom_top and bottom <= ebottom_bottom)
            if not visible and not first_block:
                break
            first_block = False
            if visible and block.isVisible():
                self._visible_blocks.append((top, block_nbr, block))
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_nbr = block.blockNumber()
        
        pprint.pprint(self._visible_blocks)

class CodeEditor(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.build()
    
    def build(self):
        self.container = QVBoxLayout(self)
        self.setLayout(self.container)
        self.container.setContentsMargins(0,0,0,0)

        self.editor_area = QHBoxLayout()
        self.editor_area.setContentsMargins(0,0,0,0)

        self.breadcrumb = Breadcrumb(self)
        self.chelly_editor = ChellyEditor(self)#GenericCodeEditor(self)

        self.editor_area.addWidget(self.chelly_editor)

        self.container.addWidget(self.breadcrumb)
        self.container.addLayout(self.editor_area)