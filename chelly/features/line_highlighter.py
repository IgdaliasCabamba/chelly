from qtpy.QtGui import QBrush
from dataclasses import dataclass
from ..core import Feature, TextDecoration, drift_color

class CaretLineHighLighter(Feature):

    @dataclass(frozen=True)
    class Defaults:
        LINE_TEXT_COLOR = False

    class Properties(Feature._Properties):
        def __init__(self, feature:Feature) -> None:
            super().__init__(feature)
            self.__line_text_color = CaretLineHighLighter.Defaults.LINE_TEXT_COLOR

        @property
        def line_text_color(self) -> bool:
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
    
    def _clear_current_deocration(self) -> None:
        if self._decoration is not None:
            self.editor.decorations.remove(self._decoration)
            self._decoration = None

    def refresh(self) -> None:
        self._clear_current_deocration()
        
        if not self.editor.properties.view_only:
            brush = QBrush(self.editor.style.theme.caret_line.background)
            self._decoration = TextDecoration(self.editor.textCursor())
            self._decoration.set_background(brush)
            self._decoration.set_full_width()
            
            if self.properties.line_text_color:
                self._decoration.set_foreground(
                    self.editor.style.theme.caret_line.foreground
                )

            self.editor.decorations.append(self._decoration)