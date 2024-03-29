from typing_extensions import Self
from typing import Any
from qtpy.QtCore import QSize
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGraphicsDropShadowEffect, QHBoxLayout
from ...core import Panel
from ...internal import chelly_property
from .editor import MiniMapEditor


class MiniMap(Panel):
    class Properties(Panel._Properties):
        def __init__(self, minimap_instance) -> None:
            super().__init__(minimap_instance)
            self.__max_width = 140
            self.__min_width = 40
            self.__width_percentage = 40
            self.__resizable = True
            self.__chelly_editor: MiniMapEditor = self.instance.chelly_editor
            self.__chelly_editor.slider.setFixedWidth(self.__max_width)
            self.__drop_shadow = None
            self.default()

        def default(self):
            drop_shadow = QGraphicsDropShadowEffect(self.instance)
            drop_shadow.setColor(QColor("#111111"))
            drop_shadow.setXOffset(-3)
            drop_shadow.setYOffset(-3)
            drop_shadow.setBlurRadius(6)
            self.shadow = drop_shadow

        @chelly_property
        def shadow(self) -> QGraphicsDropShadowEffect:
            return self.__drop_shadow

        @shadow.setter
        def shadow(self, new_shadow: QGraphicsDropShadowEffect) -> None:
            self.__drop_shadow = new_shadow
            self.instance.setGraphicsEffect(self.__drop_shadow)

        @chelly_property
        def max_width_hint(self) -> float:
            if self.resizable:
                editor_width = self.instance.editor.size().width()

                # compute percentage size
                max_width = editor_width * self.__width_percentage // 100

                if max_width > self.__max_width:
                    max_width = self.__max_width

                if max_width < self.__min_width:
                    max_width = self.__min_width

            else:
                max_width = self.__max_width

            return max_width

        @chelly_property
        def max_width(self) -> int:
            return self.__max_width

        @max_width.setter
        def max_width(self, width: int) -> None:
            self.__max_width = width
            self.__chelly_editor.slider.setFixedWidth(width)

        @chelly_property
        def min_width(self) -> int:
            return self.__min_width

        @min_width.setter
        def min_width(self, width: int) -> None:
            self.__min_width = width

        @chelly_property
        def width_percentage(self) -> int:
            return self.__width_percentage

        @width_percentage.setter
        def width_percentage(self, width: int) -> None:
            if isinstance(width, int):
                self.__width_percentage = width

        @chelly_property
        def resizable(self) -> bool:
            return self.__resizable

        @resizable.setter
        def resizable(self, value: bool) -> None:
            self.__resizable = value

    @property
    def properties(self) -> Properties:
        return self.__properties

    @properties.setter
    def properties(self, new_properties: Properties) -> None:
        if isinstance(new_properties, MiniMap.Properties):
            self.__properties = new_properties
        else:
            self.__properties = new_properties(self)

    @property
    def chelly_editor(self) -> MiniMapEditor:
        return self._minimap

    def __init__(self, editor):
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

    def update_shadow(self, force: bool = False) -> Self:
        if len(self.editor.visible_blocks) == 1 and not force:
            self.properties.shadow.setEnabled(False)

        elif (
            len(self.editor.visible_blocks) == 1
            and force
            and len(self.editor.toPlainText()) > 0
        ):
            self.properties.shadow.setEnabled(True)

        else:
            for top, block_number, block in self.editor.visible_blocks:
                width = self.editor.fontMetrics().boundingRect(block.text()).width()

                line_width = (
                    self.editor.geometry().width() - self.geometry().width()
                ) - width
                if line_width < 0:
                    self.properties.shadow.setEnabled(True)
                    break
                else:
                    self.properties.shadow.setEnabled(False)

        return self

    def update(self) -> Self:
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
        return QSize(self.properties.max_width_hint, self.fixed_size_hint)

    def __enter__(self):
        return self.chelly_editor

    def __exit__(self, *args, **kvargs) -> None:
        return None


__all__ = ["MiniMap"]
