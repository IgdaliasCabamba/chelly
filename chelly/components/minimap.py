from typing_extensions import Self
from PySide6.QtCore import QSize, Qt, QEvent
from PySide6.QtGui import (QFontMetrics, QResizeEvent)
from PySide6.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout,QFrame)

#from ..api.chelly import ChellyEditor as CodeEditor
from .code_editor import CodeEditor

from ..core import (Panel, Properties,TextEngine, Character)
import string
    
class SliderArea(QFrame):
    def __init__(self, minimap):
        super().__init__(minimap)
        self.minimap = minimap
        self.pressed = False
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.change_transparency(self.minimap.editor.style.theme.minimap.slider.no_state_color)

    def change_transparency(self, colors:tuple):
        style = string.Template("SliderArea{background-color:rgba($r,$g,$b,$a)}")
        self.setStyleSheet(
            style.substitute(
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
            self.minimap.scroll_area(pos, self.line_on_visible_area)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.change_transparency(self.minimap.editor.style.theme.minimap.slider.color)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.change_transparency(self.minimap.editor.style.theme.minimap.slider.hover_color)

class _DocumentMap(CodeEditor):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor:CodeEditor = parent.editor
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setMouseTracking(True)
        self.setTabStopDistance(QFontMetrics(
            self.font()).horizontalAdvance(Character.LARGEST.value))

        self.zoomOut(8)
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
    def mouseMoveEvent(self, event) -> None:
        pass

    def mouseReleaseEvent(self, event) -> None:
        pass

    def wheelEvent(self, event) -> None:
        self.editor.wheelEvent(event)
    
    def _update_contents(self, pos:int=0, charsrem:int=0, charsadd:int=0):
        #print(f"[{charsadd}] chars added [{charsrem}] removed at: {pos}")
        
        line_number = TextEngine(self.editor).current_line_nbr
        TextEngine(self).move_cursor_to_line(line_number)
        line_count = TextEngine(self.editor).line_count

        if self._amount_of_blocks == line_count:
            text = TextEngine(self.editor).text_at_line(line_number)
            TextEngine(self).set_text_at_line(
                self.textCursor().blockNumber(), text)
            TextEngine(self).move_cursor_to_line(line_number)
        
        elif self._amount_of_blocks == line_count-1:
            cursor = self.textCursor()
            cursor.setPosition(pos)
            cursor.insertText("\n")
            self.setTextCursor(cursor)
        
        elif self._amount_of_blocks == line_count+1:
            TextEngine(self).move_cursor_to_line(line_number+1)
            cursor = self.textCursor()
            cursor.deletePreviousChar()
            self.setTextCursor(cursor)

        else:
            self.document().setPlainText(
                self.editor.document().toPlainText()
            )
            TextEngine(self).move_cursor_to_line(
                TextEngine(self.editor).current_line_nbr
            )

        self._amount_of_blocks = TextEngine(self.editor).line_count

class MiniMapEditor(_DocumentMap):
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

    def scroll_slide(self, y_point: int):
        self.slider.move(0, y_point)

    def update_ui(self):
        row, column = TextEngine(self.editor).cursor_position
        TextEngine(self).goto_line(row, column)
        self._scroll_slide()

    def _scroll_slide(self):
        num_editor_visible_lines = TextEngine(
            self.editor).visible_lines_from_line_count
        lines_on_editor_screen = TextEngine(self.editor).visible_lines

        if num_editor_visible_lines > lines_on_editor_screen:

            self._move_scroll(num_editor_visible_lines, lines_on_editor_screen)

            editor_line_nr = TextEngine(
                self.editor).line_number_from_position(0, 0)
            delta_y = TextEngine(self).point_y_from_line_number(editor_line_nr)

            # or:
            #   higher_pos = TextEngine(self.editor).position_from_point(0,0)
            #   delta_y = TextEngine(self).point_y_from_position(higher_pos)

            self.slider.move(0, delta_y)

        self.current_scroll_value = self.editor.verticalScrollBar().value()

    def _move_scroll(self, num_editor_visible_lines, lines_on_editor_screen):
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

    def mousePressEvent(self, event) -> None:
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


class MiniMap(Panel):
    
    class Properties:
        def __init__(self, minimap_container) -> None:
            self.__minimap_container = minimap_container
            self.__max_width = 140
            self.__min_width = 40
            self.__width_percentage = 40
            self.__resizable = True
            self.__drop_shadow = None
            self.__slider_fixed_heigth = 80
            self.default()
        
        def default(self):
            drop_shadow = QGraphicsDropShadowEffect(self.__minimap_container)
            drop_shadow.setColor(self.__minimap_container.editor.style.theme.minimap.shadow_color)
            drop_shadow.setXOffset(-3)
            drop_shadow.setYOffset(-3)
            drop_shadow.setBlurRadius(6)
            self.shadow = drop_shadow
            self.__minimap_container.chelly_editor.slider.setFixedHeight(self.__slider_fixed_heigth)
            self.__minimap_container.chelly_editor.slider.setFixedWidth(self.__minimap_container.size().width())
        
        @property
        def shadow(self) -> QGraphicsDropShadowEffect:
            return self.__drop_shadow
        
        @shadow.setter
        def shadow(self, new_shadow: QGraphicsDropShadowEffect) -> None:
            if isinstance(new_shadow, QGraphicsDropShadowEffect):
                self.__drop_shadow = new_shadow
                self.__minimap_container.setGraphicsEffect(self.__drop_shadow)
        
        @property
        def max_width(self) -> int:
            if self.resizable:
                editor_width = self.__minimap_container.editor.size().width()
                
                #compute percentage size
                max_width = editor_width * self.__width_percentage // 100

                if max_width > self.__max_width:
                    max_width = self.__max_width
                
                if max_width < self.__min_width:
                    max_width = self.__min_width

            else:
                max_width = self.__max_width
            
            self.__minimap_container.chelly_editor.slider.setFixedWidth(max_width)
            return max_width
        
        @max_width.setter
        def max_width(self, width:int) -> None:
            if isinstance(width, int):
                self.__max_width = width
        
        @property
        def min_width(self) -> int:
            return self.__min_width
        
        @min_width.setter
        def min_width(self, width:int) -> None:
            if isinstance(width, int):
                self.__min_width = width
            
        @property
        def width_percentage(self) -> int:
            return self.__width_percentage
        
        @width_percentage.setter
        def width_percentage(self, width:int) -> None:
            if isinstance(width, int):
                self.__width_percentage = width
        
        @property
        def resizable(self) -> int:
            return self.__resizable
        
        @resizable.setter
        def resizable(self, value:bool) -> None:
            if isinstance(value, bool):
                self.__resizable = value
            
        @property
        def slider_heigth(self) -> QSize:
            return self.__slider_fixed_heigth
        
        @slider_heigth.setter
        def slider_fixed_heigth(self, size:QSize) -> None:
            self.__slider_fixed_heigth = size
            self.__minimap_container.chelly_editor.slider.setFixedHeight(self.__slider_fixed_heigth)

    def __init__(self, editor, properties:Properties = None):
        super().__init__(editor)

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._minimap = MiniMapEditor(self)

        self.box.addWidget(self._minimap)
        self.setLayout(self.box)

        self.__properties = MiniMap.Properties(self)
        self.editor.blockCountChanged.connect(self.update_shadow)
        self.editor.on_resized.connect(self.update_shadow)
        self.editor.on_text_setted.connect(self.update_shadow)
        self.update_shadow(True)
    
    @property
    def chelly_editor(self) -> MiniMapEditor:
        return self._minimap
    
    @property
    def properties(self) -> Properties:
        return self.__properties
    
    @properties.setter
    def properties(self, new_properties:Properties) -> None:
        if isinstance(new_properties, Properties):
            self.__properties = new_properties
    
    def update_shadow(self, force:bool = False) -> Self:
        if len(self.editor.visible_blocks) == 1 and not force:
            self.properties.shadow.setEnabled(False)
        
        elif len(self.editor.visible_blocks) == 1 and force and len(self.editor.toPlainText()) > 0:
            self.properties.shadow.setEnabled(True)
        
        else:
            for top, block_number, block in self.editor.visible_blocks:
                width = (
                    self.editor.fontMetrics()
                    .boundingRect(block.text())
                    .width()
                )

                line_width = (self.editor.geometry().width() - self.geometry().width()) - width
                if line_width < 0:
                    self.properties.shadow.setEnabled(True)
                    break
                else:
                    self.properties.shadow.setEnabled(False)

        return self

    def update(self) -> Self:
        self.properties.shadow.setColor(self.editor.style.theme.minimap.shadow_color)
        super().update()
        return self

    def activate_shadow(self):
        self._minimap.setGraphicsEffect(self.properties.shadow)

    def disable_shadow(self):
        self._minimap.setGraphicsEffect(None)
    
    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the right, we only need
        to compute the width
        """
        return QSize(self.properties.max_width, self.fixed_size_hint)
    
    def __enter__(self):
        return self.chelly_editor
    
    def __exit__(self, *args, **kvargs) -> None:
        return None