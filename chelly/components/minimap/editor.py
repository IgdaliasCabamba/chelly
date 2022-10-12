from qtpy.QtCore import QEvent
from qtpy.QtGui import QMouseEvent, QResizeEvent
from ...core import TextEngine
from .slider import SliderArea
from .document import DocumentMap
from math import modf

class MiniMapEditor(DocumentMap):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.__cached_height = self.height()
        self.__cached_max_scroll_y = self.editor.verticalScrollBar().maximum()
        
        self.slider = SliderArea(self)
        self.slider.show()
        
        self.bind()
    
    def bind(self):
        self.editor.document().contentsChange.connect(self._update_contents)
        self.editor.on_painted.connect(self.update_ui)
        self.slider.on_scroll_area.connect(self.scroll_editor)
        self.editor.verticalScrollBar().rangeChanged.connect(self._update_scrollbar_cache)
    
    def _update_scrollbar_cache(self):
        self.__cached_max_scroll_y = self.editor.verticalScrollBar().maximum()

    def update_ui(self):
        line = TextEngine(self.editor).current_line_nbr
        TextEngine(self).goto_line(line)
        self._scroll_slide()

    def _scroll_slide(self):
        num_editor_visible_lines = TextEngine(self.editor).visible_lines_from_line_count
        lines_on_editor_screen = TextEngine(self.editor).visible_lines

        if num_editor_visible_lines > lines_on_editor_screen:
            
            self._move_scroll_bar()
            
            if not self.slider.is_pressed:
                
                max_height = self.__cached_height
                current_scroll_y = self.editor.verticalScrollBar().value()
                max_scroll_y = self.__cached_max_scroll_y
                
                delta_y = current_scroll_y - (self.slider.height() // 2)

                if max_scroll_y > max_height:
                    decimal_delta_y = max_scroll_y / max_height
            
                    if modf(decimal_delta_y)[0] <= 0.5:
                        decimal_delta_y += 1
                    else:
                        decimal_delta_y += 0.5

                    py = current_scroll_y // decimal_delta_y                    
                    delta_y = py - (self.slider.height() // 2)
                
                if delta_y <0:
                    delta_y = 0

                self.slider.scroll_y(delta_y)
        

    def scroll_editor(self, y_pos) -> None:
        max_height = self.__cached_height
        max_scroll_y = self.__cached_max_scroll_y
        delta_y = y_pos

        if max_scroll_y > max_height:
            decimal_delta_y = max_scroll_y / max_height
            
            if modf(decimal_delta_y)[0] <= 0.5:
                decimal_delta_y += 1
            else:
                decimal_delta_y += 0.5

            delta_y = y_pos * int(decimal_delta_y)

        self.editor.verticalScrollBar().setValue(delta_y)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        TextEngine(self.editor).move_cursor_to_line(
            TextEngine(self).line_number_from_position(
                y_pos = event.pos().y(),
                x_pos = event.pos().x()
            )
        )
    
    def leaveEvent(self, event: QEvent) -> None:
        self.slider.change_transparency(self.editor.style.theme.minimap.slider.no_state_color)
        return super().leaveEvent(event)
    
    def enterEvent(self, event: QEvent) -> None:
        self.slider.change_transparency(self.editor.style.theme.minimap.slider.color)
        return super().enterEvent(event)
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__cached_height = self.height()
        return super().resizeEvent(event)
    
    def _move_scroll_bar(self):
        max_scroll_y = self.__cached_max_scroll_y

        dy = max_scroll_y / (self.editor.verticalScrollBar().value()+1)
        if dy <= 0:
            dy = 1

        self.verticalScrollBar().setValue(self.editor.verticalScrollBar().value()//dy)