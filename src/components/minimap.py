from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QScrollBar
from PyQt6.QtCore import Qt
from ..core import CONSTS

class ScrollBar(QScrollBar):
    def __init__(self, editor, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.editor = editor
        self.sliderMoved.connect(self.moved)

    def moved(self):
        self.editor.verticalScrollBar().setValue(self.value())

    def update_position(self):
        self.setValue(self.editor.verticalScrollBar().value())
        self.setRange(0, self.editor.verticalScrollBar().maximum())

class SliderArea(QWidget):
    def __init__(self, minimap):
        super().__init__(minimap)
        self.minimap = minimap
        self.pressed = False
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.change_transparency(CONSTS.MINIMAP_SLIDER_OPACITY_MIN)
        self.setFixedSize(CONSTS.MINIMAP_SLIDER_AREA_FIXED_SIZE)

    def change_transparency(self, bg: int):
        self.setStyleSheet(
            "#minimap-slider{background-color:rgba(255,255,255,%d)}" % bg
        )

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressed = True
        self.setCursor(Qt.ClosedHandCursor)
        
        first_visible_line = self.minimap.editor.firstVisibleBlock()

        pos_parent = self.mapToParent(event.pos())
        position = self.minimap.SendScintilla(
            QsciScintilla.SCI_POSITIONFROMPOINT, pos_parent.x(), pos_parent.y()
        )
        line = self.minimap.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, position)
        self.line_on_visible_area = (line - first_visible_line) + 1

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.pressed = False
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.pressed:
            pos = self.mapToParent(event.pos())
            self.minimap.scroll_area(pos, self.line_on_visible_area)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.change_transparency(iconsts.MINIMAP_SLIDER_OPACITY_MID)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.change_transparency(iconsts.MINIMAP_SLIDER_OPACITY_MAX)



class MiniMap(QPlainTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor = parent
        self.zoomOut(0)
        self.setMouseTracking(True)
        self.slider = SliderArea(self)
        self.slider.show()
    
    def scroll_map(self):
        pass

    def shutdown(self):
        self.setDocument(None)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        super().wheelEvent(event)
        self.editor.wheelEvent(event)

class MinimapBox(QWidget):
    pass