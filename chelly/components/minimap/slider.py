from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QResizeEvent, QColor
from qtpy.QtWidgets import QFrame
from ...core import Panel
import string
from typing import Any
    
class SliderArea(QFrame):

    class Styles(Panel._Styles):
        def __init__(self, instance: Any) -> None:
            super().__init__(instance)
            self._hover_color:tuple = (255, 255, 255, 30)
            self._color:tuple = (255, 255, 255, 15)
            self._no_state_color:tuple = (255, 255, 255, 0)

        @property
        def color(self) -> tuple:
            return self._color
    
        @color.setter
        def color(self, new_color:tuple) -> None:
            self._color = new_color

        @property
        def no_state_color(self) -> tuple:
            return self._no_state_color
        
        @no_state_color.setter
        def no_state_color(self, new_color:QColor) -> None:
            self._no_state_color = new_color
        
        @property
        def hover_color(self) -> tuple:
            return self._hover_color
    
        @hover_color.setter
        def hover_color(self, new_color:QColor) -> None:
            self._hover_color = new_color
        
    class Properties(Panel._Properties):
        def __init__(self, instance: Any) -> None:
            super().__init__(instance)
            self.__slider_fixed_heigth = 80
            self.instance.setFixedHeight(self.__slider_fixed_heigth)

        @property
        def slider_heigth(self) -> int:
            return self.__slider_fixed_heigth
        
        @slider_heigth.setter
        def slider_fixed_heigth(self, size:int) -> None:
            self.__slider_fixed_heigth = size
            self.instance.setFixedHeight(self.__slider_fixed_heigth)

    @property
    def styles(self) -> Styles:
        return self.__styles
        
    @styles.setter
    def styles(self, new_styles:Styles) -> None:
        self.__styles = new_styles
    
    @property
    def properties(self) -> Properties:
        return self.__properties
    
    @properties.setter
    def properties(self, new_properties:Properties) -> None:
        if isinstance(new_properties, SliderArea.Properties):
            self.__properties = new_properties

    on_scroll_area = Signal(int)
    style_template = string.Template("SliderArea{background-color:rgba($r,$g,$b,$a)}")

    def __init__(self, minimap):
        super().__init__(minimap)
        self.minimap = minimap
        self.__pressed = False
        self.__properties = SliderArea.Properties(self)
        self.__styles = SliderArea.Styles(self)
        self.__cached_height = self.height()
        self.__cached_minimap_height = self.minimap.height()
        
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.change_transparency(self.styles.no_state_color)
    
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
        self.change_transparency(self.styles.color)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.change_transparency(self.styles.hover_color)
    
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
            return self.move_y(0)

        if delta_plus > minimap_height:
            self.move_y(virtual_y_point)
            return self.move_y(minimap_height-height)
            
        self.move_y(virtual_y_point)
    
    def move_y(self, y_pos:int):
        self.move(0, int(y_pos))