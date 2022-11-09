from qtpy.QtGui import QBrush, QColor
from qtpy.QtCore import Qt
from typing import Any
from dataclasses import dataclass
from ..core import Feature, TextDecoration, drift_color
from ..internal import chelly_property, ChellyShareableSetting, ChellyShareableStyle

class CaretLineHighLighter(Feature):

    @dataclass(frozen=True)
    class Defaults:
        LINE_TEXT_COLOR = False        

    class Properties(Feature._Properties):
        def __init__(self, feature:Feature) -> None:
            super().__init__(feature)
            self.__line_text_color = CaretLineHighLighter.Defaults.LINE_TEXT_COLOR

            self._background = QColor(Qt.GlobalColor.darkBlue)
            self._background.setAlpha(70)
            self._foreground = QColor(Qt.GlobalColor.white)
        
        @chelly_property(value_type=QColor)
        def foreground(self) -> ChellyShareableStyle:
            return self._foreground

        @foreground.setter
        def foreground(self, new_color: QColor) -> None:
            self._foreground = new_color

        @chelly_property(value_type=QColor)
        def background(self) -> ChellyShareableStyle:
            return self._background

        @background.setter
        def background(self, new_color: QColor) -> None:
            self._background = new_color

        @chelly_property(value_type=bool)
        def line_text_color(self) -> ChellyShareableSetting:
            return self.__line_text_color
        
        @line_text_color.setter
        def line_text_color(self, value:bool) -> None:
            self.__line_text_color = value
    
    @property
    def properties(self) -> Properties:
        return self.__properties
    
    @properties.setter
    def properties(self, new_properties:Properties) -> Properties:
        if new_properties is CaretLineHighLighter.Properties:
            self.__properties = new_properties(self)

        elif isinstance(new_properties, CaretLineHighLighter.Properties):
            self.__properties = new_properties
    

    def __init__(self, editor):
        super().__init__(editor)
        self.__properties = CaretLineHighLighter.Properties(self)

        self._decoration = None
        self.editor.cursorPositionChanged.connect(self.refresh)
        self.editor.on_text_setted.connect(self.refresh)
        self.refresh()
    
    def _clear_current_decoration(self) -> None:
        if self._decoration is not None:
            self.editor.decorations.remove(self._decoration)
            self._decoration = None

    def refresh(self) -> None:
        self._clear_current_decoration()
        
        if not self.editor.properties.view_only:
            brush = QBrush(self.properties.background)
            self._decoration = TextDecoration(self.editor.textCursor())
            self._decoration.set_background(brush)
            self._decoration.set_full_width()
            
            if self.properties.line_text_color:
                self._decoration.set_foreground(
                    self.properties.foreground
                )

            self.editor.decorations.append(self._decoration)