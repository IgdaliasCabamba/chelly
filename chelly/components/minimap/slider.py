from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QResizeEvent
from qtpy.QtWidgets import QFrame
from ...core import TextEngine
import string
    
class SliderArea(QFrame):

    on_scroll_area = Signal(int)
    style_template = string.Template("SliderArea{background-color:rgba($r,$g,$b,$a)}")

    def __init__(self, minimap):
        super().__init__(minimap)
        self.minimap = minimap
        self.__pressed = False
        self.global_style = self.minimap.editor.style.theme.minimap
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.change_transparency(self.global_style.slider.no_state_color)
        self.__cached_height = self.height()
        self.__cached_minimap_height = self.minimap.height()
    
    @property
    def is_pressed(self) -> bool:
        return self.__pressed

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
        self.setCursor(Qt.ClosedHandCursor)
        self.__pressed = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.__pressed = False
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.__pressed:
            pos = self.mapToParent(event.pos())
            y_pos = pos.y()
            self.scroll_with_cursor(y_pos)
            self.on_scroll_area.emit(y_pos)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.change_transparency(self.global_style.slider.color)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.change_transparency(self.global_style.slider.hover_color)
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__cached_height = self.height()
        self.__cached_minimap_height = self.minimap.height()
        return super().resizeEvent(event)
    
    def scroll_with_cursor(self, y_point: int):
        height = self.__cached_height
        minimap_height = self.__cached_minimap_height
        
        virtual_y_point = y_point - (height // 2) # center cursor on it
        delta_plus = y_point + height

        if y_point < 0:
            return self.scroll_y(0)

        if delta_plus > minimap_height:
            self.scroll_y(virtual_y_point)
            return self.scroll_y(minimap_height-height)
            
        self.scroll_y(virtual_y_point)
    
    def scroll_y(self, y_pos:int):
        self.move(0, y_pos)
