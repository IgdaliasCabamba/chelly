from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QFrame
from ...core import TextEngine
import string
    
class SliderArea(QFrame):

    on_scroll_area = Signal(object, object)
    style_template = string.Template("SliderArea{background-color:rgba($r,$g,$b,$a)}")

    def __init__(self, minimap):
        super().__init__(minimap)
        self.minimap = minimap
        self.pressed = False
        self.global_style = self.minimap.editor.style.theme.minimap
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.change_transparency(self.global_style.slider.no_state_color)

    def change_transparency(self, colors:tuple):
        self.setStyleSheet(
            self.style_template.substitute(
                r=colors[0],
                g=colors[1],
                b=colors[2],
                a=colors[3])
        )

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressed = True
        self.setCursor(Qt.ClosedHandCursor)
        first_visible_line = TextEngine(self.minimap.editor).first_visible_line

        pos_parent = self.mapToParent(event.pos())
        line = TextEngine(self.minimap).line_number_from_position(y_pos = pos_parent.y(), x_pos = pos_parent.x())
        self.line_on_visible_area = (line - first_visible_line) + 1

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.pressed = False
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.pressed:
            pos = self.mapToParent(event.pos())
            self.on_scroll_area.emit(pos, self.line_on_visible_area)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.change_transparency(self.global_style.slider.color)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.change_transparency(self.global_style.slider.hover_color)
    
    def scroll(self, y_point: int):
        self.move(0, y_point)