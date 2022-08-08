from PySide6.QtWidgets import QScrollBar, QFrame
from PySide6.QtCore import Qt, QSize
from ..core import TextFunctions

class iconsts:
    MINIMAP_MINIMUM_ZOOM: int = -10
    MINIMAP_CURSOR: int = 8
    MINIMAP_EXTRA_ASCENT: int = 0
    MINIMAP_EXTRA_DESCENT: int = 0
    MINIMAP_FIXED_WIDTH = 140
    MINIMAP_BOX_FIXED_WIDTH = 140
    MINIMAP_SLIDER_OPACITY_MIN = 0
    MINIMAP_SLIDER_OPACITY_MID = 15
    MINIMAP_SLIDER_OPACITY_MAX = 30
    MINIMAP_SLIDER_AREA_FIXED_SIZE = QSize(140, 80)
    MINIMAP_SHADOW_MIN_TEXT_WIDTH = 50
    MINIMAP_BOX_SHADOW_BLURRADIUS = 12
    MINIMAP_BOX_SHADOW_Y_OFFSET = -3
    MINIMAP_BOX_SHADOW_X_OFFSET = 0


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

class SliderArea(QFrame):
    def __init__(self, minimap):
        super().__init__(minimap)
        self.setObjectName("minimap-slider")
        self.minimap = minimap
        self.pressed = False
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.change_transparency(iconsts.MINIMAP_SLIDER_OPACITY_MIN)
        self.setFixedSize(iconsts.MINIMAP_SLIDER_AREA_FIXED_SIZE)

    def change_transparency(self, bg: int):
        self.setStyleSheet(
            "#minimap-slider{background-color:rgba(255,255,255,%d)}" % bg
        )

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressed = True
        self.setCursor(Qt.ClosedHandCursor)
        first_visible_line = self.minimap.editor.firstVisibleBlock().firstLineNumber()

        pos_parent = self.mapToParent(event.pos())
        line = TextFunctions(self.minimap).get_line_nbr_from_position(pos_parent.x(), pos_parent.y())
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
