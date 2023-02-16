from typing import Any, Union

from ..core import TextEngine, Feature, FontEngine, Character, ChellyCache
from ..internal import chelly_property
from qtpy.QtGui import QPen, QColor, QPaintEvent, QPainter
from dataclasses import dataclass


class EdgeLine(Feature):
    @dataclass(frozen=True)
    class Defaults:
        LINE_COVER_VIEW_SIZE = 2**16
        LINE_POS = 80
        LINE_COLOR = QColor("#72c3f0")

    class Properties(Feature._Properties):
        def __init__(self, feature: Feature) -> None:
            super().__init__(feature)
            self.__margin_pos = EdgeLine.Defaults.LINE_POS

            self.__color = EdgeLine.Defaults.LINE_COLOR
            self._pen = QPen(self.color)

        @chelly_property
        def pen(self) -> QPen:
            return self._pen

        @chelly_property
        def color(self) -> QColor:
            return self.__color

        @color.setter
        def color(self, value: QColor) -> None:
            self.__color = value
            self._pen = QPen(self.__color)
            TextEngine(self.feature.editor).mark_whole_doc_dirty()  # TODO
            self.feature.editor.repaint()

        @chelly_property
        def position(self) -> int:
            return self.__margin_pos

        @position.setter
        def position(self, value: int) -> None:
            self.__margin_pos = value

    @property
    def properties(self) -> Properties:
        return self.__properties

    @properties.setter
    def properties(self, new_properties: Properties) -> Properties:
        if new_properties is EdgeLine.Properties:
            self.__properties = new_properties(self)

        elif isinstance(new_properties, EdgeLine.Properties):
            self.__properties = new_properties

    def __init__(self, editor):
        super().__init__(editor)
        self.__properties = EdgeLine.Properties(self)
        self.__cached_cursor_position = ChellyCache(
            None, None, lambda: TextEngine(self.editor).cursor_position
        )

        self.editor.on_painted.connect(self._paint_margin)
        self.editor.repaint()

    def _paint_margin(self, event: QPaintEvent) -> None:
        if not self.__cached_cursor_position.changed:
            return None

        offset = (
            self.editor.contentOffset().x() + self.editor.document().documentMargin()
        )
        line_x_point = (
            FontEngine(self.editor.font()).real_horizontal_advance(
                Character.LARGEST.value, min_zero=True
            )
            * self.properties.position
        )
        line_x_point += offset
        int_line_x_point = int(line_x_point)

        with QPainter(self.editor.viewport()) as painter:
            painter.setPen(self.properties.pen)
            painter.drawLine(
                int_line_x_point,
                0,
                int_line_x_point,
                EdgeLine.Defaults.LINE_COVER_VIEW_SIZE,
            )


__all__ = ["EdgeLine"]
