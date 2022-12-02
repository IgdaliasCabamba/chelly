from ..core import Feature, TextEngine
from ..internal import chelly_property, ChellyFollowedValue
from qtpy.QtCore import Qt

#!warning: Unstable

class CursorScroller(Feature):
    
    LINE_NUMBER_DELTA = 2

    def __init__(self, editor):
        super().__init__(editor)
        self.editor.on_key_pressed.connect(self.natural_scroll)
        self.editor.verticalScrollBar().valueChanged.connect(self.restore)
    
    def update_scroll(self, state:bool) -> None:
        self.editor.setCenterOnScroll(state)
        minimap = self.editor.panels.get("MiniMap")
        if minimap is not None:
            minimap.chelly_editor.setCenterOnScroll(state)

    
    def restore(self, *args, **kwargs):
        self.update_scroll(True)
    
    @property
    def current_line_number_down(self) -> int:
        return TextEngine(self.editor).current_line_nbr + CursorScroller.LINE_NUMBER_DELTA
    
    @property
    def current_line_number_up(self) -> int:
        return TextEngine(self.editor).current_line_nbr
    
    @property
    def natural_scroll_limit(self):
        return (TextEngine(self.editor).line_count + 5) - (TextEngine(self.editor).amount_of_visible_blocks//2)
    
    def natural_scroll(self, event):
        if event.key() == Qt.Key_Down:
            if self.current_line_number_down == self.editor.visible_blocks[-1][1]:
                if self.editor.visible_blocks[-1][1] < self.natural_scroll_limit:
                    self.update_scroll(False)
                else:
                    self.update_scroll(True)
            else:
                self.update_scroll(True)
        
        elif event.key() == Qt.Key_Up:
            if self.current_line_number_up == self.editor.visible_blocks[0][1]:
                self.update_scroll(False)
            else:
                self.update_scroll(True)
        
        else:
            self.restore()