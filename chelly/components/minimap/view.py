from typing_extensions import Self
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QGraphicsDropShadowEffect, QHBoxLayout
from ...core import Panel, Properties
from .editor import MiniMapEditor


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