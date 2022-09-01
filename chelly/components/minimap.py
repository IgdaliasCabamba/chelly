from typing_extensions import Self
import PySide6
from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import (QColor, QFont, QFontMetrics, QPainter, QTextBlock,
                           QTextCursor, QTextOption)
from PySide6.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout,
                               QPlainTextEdit, QScrollBar, QFrame)

#from ..api.chelly import ChellyEditor as CodeEditor
from .code_editor import CodeEditor

from ..core import (FeaturesExceptions, LexerExceptions, Panel, Properties,
                    PropertiesExceptions, TextEngine)
from ..managers import FeaturesManager, LanguagesManager
import string

class iconsts:
    MINIMAP_MINIMUM_ZOOM: int = -10
    MINIMAP_SLIDER_AREA_FIXED_SIZE = QSize(140, 80)
    MINIMAP_SHADOW_MIN_TEXT_WIDTH = 50
    MINIMAP_BOX_SHADOW_BLURRADIUS = 12
    MINIMAP_BOX_SHADOW_Y_OFFSET = -3
    MINIMAP_BOX_SHADOW_X_OFFSET = 0

class SliderArea(QFrame):
    def __init__(self, minimap):
        super().__init__(minimap)
        self.minimap = minimap
        self.pressed = False
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.change_transparency(self.minimap.editor.style.theme.minimap.slider_no_state_color)
        self.setFixedSize(iconsts.MINIMAP_SLIDER_AREA_FIXED_SIZE)

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
        self.change_transparency(self.minimap.editor.style.theme.minimap.slider_color)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.change_transparency(self.minimap.editor.style.theme.minimap.slider_hover_color)


class MiniMap(CodeEditor):
    def __init__(self, parent):
        super().__init__(parent)

        self.editor = parent.editor
        self._amount_of_blocks = TextEngine(self.editor).line_count
        self.current_scroll_value = self.editor.verticalScrollBar().value()

        self.setTextInteractionFlags(Qt.NoTextInteraction)

        self.slider = SliderArea(self)
        self.slider.show()

        self.setMouseTracking(True)
        self.setTabStopDistance(QFontMetrics(
            self.font()).horizontalAdvance('W'))

        self.zoomOut(8)
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.editor.document().contentsChange.connect(self.update_contents)
        self.editor.on_painted.connect(self.update_ui)

    def scroll_slide(self, y_point: int):
        self.slider.move(0, y_point)

    def update_ui(self):
        self._scroll_slide()

    def update_contents(self, pos, charsrem, charsadd):
        line_number = TextEngine(self.editor).current_line_nbr
        TextEngine(self).move_cursor_to_line(line_number)
        text = TextEngine(self.editor).text_at_line(line_number)

        if self._amount_of_blocks == TextEngine(self.editor).line_count:
            TextEngine(self).set_text_at_line(
                self.textCursor().blockNumber(), text)
            TextEngine(self).move_cursor_to_line(line_number)
        else:
            self.document().setPlainText(
                self.editor.document().toPlainText()
            )
            TextEngine(self).move_cursor_to_line(
                TextEngine(self.editor).current_line_nbr
            )

        self._amount_of_blocks = TextEngine(self.editor).line_count

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
        super().mousePressEvent(event)
        TextEngine(self.editor).move_cursor_to_line(
            TextEngine(self).line_number_from_position(
                y_pos = event.pos().y(),
                x_pos = event.pos().x()
            )
        )

    def wheelEvent(self, event) -> None:
        super().wheelEvent(event)
        self.editor.wheelEvent(event)
    
    def leaveEvent(self, event: PySide6.QtCore.QEvent) -> None:
        self.slider.change_transparency(self.editor.style.theme.minimap.slider_no_state_color)
        return super().leaveEvent(event)
    
    def enterEvent(self, event: PySide6.QtCore.QEvent) -> None:
        self.slider.change_transparency(self.editor.style.theme.minimap.slider_color)
        return super().enterEvent(event)


class MiniChellyMap(Panel):
    
    class Properties:
        def __init__(self, minimap_container) -> None:
            self.__minimap_container = minimap_container
            self.__max_width:int = 140
            self.__min_width:int = 40
            self.__resizable:bool = True
            self.__drop_shadow = None
            self.default()
        
        def default(self):
            drop_shadow = QGraphicsDropShadowEffect(self.__minimap_container)
            drop_shadow.setColor(self.__minimap_container.editor.style.theme.minimap.shadow_color)
            drop_shadow.setXOffset(-3)
            drop_shadow.setYOffset(1)
            drop_shadow.setBlurRadius(6)
            self.shadow = drop_shadow
        
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
            return self.__max_width
        
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
        def resizable(self) -> int:
            return self.__resizable
        
        @resizable.setter
        def resizable(self, value:bool) -> None:
            if isinstance(value, bool):
                self.__resizable = value


    def __init__(self, editor, properties:Properties = None):
        super().__init__(editor)
        self.__properties = MiniChellyMap.Properties(self)

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._minimap = MiniMap(self)

        self.box.addWidget(self._minimap)
        self.setLayout(self.box)
    
    @property
    def code_viewer(self) -> MiniMap:
        return self._minimap
    
    @property
    def properties(self) -> Properties:
        return self.__properties
    
    @properties.setter
    def properties(self, new_properties:Properties) -> None:
        if isinstance(new_properties, Properties):
            self.__properties = new_properties
    
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
        return self.code_viewer
    
    def __exit__(self, *args, **kvargs) -> None:
        return None