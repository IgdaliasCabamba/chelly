from qtpy.QtCore import QEvent
from qtpy.QtGui import QMouseEvent
from ...core import TextEngine
from .slider import SliderArea
from .document import DocumentMap

class MiniMapEditor(DocumentMap):
    def __init__(self, parent):
        super().__init__(parent)

        self._amount_of_blocks = TextEngine(self.editor).line_count
        self.current_scroll_value = self.editor.verticalScrollBar().value()

        self.slider = SliderArea(self)
        self.slider.show()
        
        self.bind()
    
    def bind(self):
        self.editor.document().contentsChange.connect(self._update_contents)
        self.editor.on_painted.connect(self.update_ui)
        self.slider.on_scroll_area.connect(self.scroll_area)

    def update_ui(self):
        line = TextEngine(self.editor).current_line_nbr
        TextEngine(self).goto_line(line)
        self._scroll_slide()

    def _scroll_slide(self):
        num_editor_visible_lines = TextEngine(
            self.editor).visible_lines_from_line_count
        lines_on_editor_screen = TextEngine(self.editor).visible_lines

        if num_editor_visible_lines > lines_on_editor_screen:

            self._move_scroll_bar(num_editor_visible_lines, lines_on_editor_screen)

            #editor_line_nr = TextEngine(
                #self.editor).line_number_from_position(0, 0)
            #delta_y = TextEngine(self).point_y_from_line_number(editor_line_nr)

            #or:
            higher_pos = TextEngine(self.editor).position_from_point(0,0)
            delta_y = TextEngine(self).point_y_from_position(higher_pos)

            self.slider.scroll(delta_y)

        self.current_scroll_value = self.editor.verticalScrollBar().value()

    def _move_scroll_bar(self, num_editor_visible_lines, lines_on_editor_screen):
        editor_first_visible_line = TextEngine(self.editor).first_visible_line
        editor_last_top_visible_line = num_editor_visible_lines - lines_on_editor_screen

        num_visible_lines = TextEngine(self).visible_lines_from_line_count
        lines_on_screen = TextEngine(self).visible_lines

        last_top_visible_line = num_visible_lines - lines_on_screen

        portion = editor_first_visible_line / editor_last_top_visible_line
        first_visible_line = round(last_top_visible_line * portion)

        self.verticalScrollBar().setValue(first_visible_line)

    def scroll_area(self, pos_parent, line_area) -> None:
        line = TextEngine(self).line_number_from_position(
            y_pos = pos_parent.y(),
            x_pos = pos_parent.x()
        )
        self.editor.verticalScrollBar().setValue(line - line_area)

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