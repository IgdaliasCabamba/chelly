from typing import Any
from dataclasses import dataclass
from qtpy.QtGui import QFont, QPainter, QPen, QColor
from qtpy.QtCore import Qt, QSize, QObject, Signal, QThread
from ...core import Panel, FontEngine, TextEngine, ChellyCache, DelayJobRunner
from ...internal import chelly_property, ChellyQThreadManager
import difflib
from nemoize import memoize


class EditionMarginWorker(QObject):
    on_compared = Signal(list)

    def __init__(self, edition_margin):
        super().__init__()
        self.edition_margin = edition_margin
        self.differ = difflib.Differ()

    def run(self):
        self.edition_margin.on_compare_request.connect(self.compare)

    def compare(self, text1: str, text2: str):
        self.on_compared.emit(list(self.differ.compare(text1, text2)))


class EditionMargin(Panel):
    on_compare_request = Signal(list, list)

    @dataclass(frozen=True)
    class Defaults:
        SHOW_TEXT_HELP = False
        MAX_LINES_COUNT = 1000

    class Properties(Panel._Properties):
        def __init__(self, panel: Panel):
            super().__init__(panel)

            self._unknow = Qt.GlobalColor.darkCyan
            self._added = Qt.GlobalColor.darkGreen
            self._removed = Qt.GlobalColor.darkRed

            self.__show_text_help = EditionMargin.Defaults.SHOW_TEXT_HELP
            self.__max_lines_count = EditionMargin.Defaults.MAX_LINES_COUNT

        @chelly_property
        def show_text_help(self) -> bool:
            return self.__show_text_help

        @show_text_help.setter
        def show_text_help(self, show: bool) -> None:
            self.__show_text_help = show

        @chelly_property
        def max_lines_count(self) -> int:
            return self.__max_lines_count

        @max_lines_count.setter
        def max_lines_count(self, limit: int) -> None:
            self.__max_lines_count = limit

        @chelly_property
        def unknow(self) -> QColor:
            return self._unknow

        @unknow.setter
        def unknow(self, color: QColor) -> None:
            self._unknow = color

        @chelly_property
        def added(self) -> QColor:
            return self._added

        @added.setter
        def added(self, color: QColor) -> None:
            self._added = color

        @chelly_property
        def removed(self) -> QColor:
            return self._removed

        @removed.setter
        def removed(self, color: QColor) -> None:
            self._removed = color

    @property
    def properties(self) -> Properties:
        return self.__properties

    @properties.setter
    def properties(self, new_properties: Properties) -> Properties:
        if new_properties is EditionMargin.Properties:
            self.__properties = new_properties(self)

        elif isinstance(new_properties, EditionMargin.Properties):
            self.__properties = new_properties

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.scrollable = True
        self.number_font = QFont()

        self.__cached_lines_text = []
        self.__cached_cursor_position = ChellyCache(
            None, None, lambda: TextEngine(self.editor).cursor_position
        )
        self.__preloaded_diff = []
        self.__properties = EditionMargin.Properties(self)

        self.thread_manager = ChellyQThreadManager()

        self.job_delayer = DelayJobRunner(200)  # ? 0.2 seconds

        self.thread = QThread()
        self.thread_manager.append(self.thread)
        self.comparasion_worker = EditionMarginWorker(self)
        self.comparasion_worker.moveToThread(self.thread)
        self.thread.started.connect(self.comparasion_worker.run)
        self.thread.start()

        self.comparasion_worker.on_compared.connect(self.preload_diffs)
        self.editor.textChanged.connect(
            lambda: self.job_delayer.request_job(self.update_diffs)
        )

    def sizeHint(self):
        """
        Returns the panel size hint (as the panel is on the left, we only need
        to compute the width
        """
        return QSize(self.lines_area_width, 0)

    @property
    def lines_area_width(self) -> int:
        space = FontEngine(self.editor.font()).real_horizontal_advance("|", True)

        return space

    def update_diffs(self):
        if self.editor.blockCount() <= 1:
            return None

        cached_lines_text_length = len(self.__cached_lines_text)
        if cached_lines_text_length >= self.properties.max_lines_count:
            return None

        first_visible_block_number = self.editor.firstVisibleBlock().blockNumber()
        lines_text = []

        first_block = self.editor.document().firstBlock()

        if not self.__cached_lines_text:
            if self.editor.blockCount() > self.properties.max_lines_count:
                return None

            for text_block in list(
                TextEngine(self.editor).iterate_blocks_from(first_block)
            ):
                lines_text.append(text_block.text())

            self.__cached_lines_text = lines_text.copy()
            return None

        else:
            for text_block in list(
                TextEngine(self.editor).iterate_blocks_from(
                    first_block, cached_lines_text_length
                )
            ):
                lines_text.append(text_block.text())

        if self.__cached_cursor_position.changed:
            self.on_compare_request.emit(self.__cached_lines_text, lines_text)

    def preload_diffs(self, diff: list) -> None:
        self.__preloaded_diff = diff

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        if not self.__preloaded_diff:
            return None

        pen = QPen()
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setWidth(8)
        point_x = 0

        height = self.editor.fontMetrics().height()

        if self.editor.firstVisibleBlock().blockNumber() <= len(
            self.__cached_lines_text
        ):
            with QPainter(self) as painter:
                for idx, diff in enumerate(self.__preloaded_diff):
                    if diff.startswith(("-", "+", "?")):
                        top = TextEngine(self.editor).point_y_from_line_number(idx)

                        if diff.startswith("-"):
                            pen.setBrush(self.properties.removed)
                            painter.setPen(pen)
                            if self.properties.show_text_help:
                                painter.drawText(6, top + height // 1.5, "!")

                        elif diff.startswith("+"):
                            pen.setBrush(self.properties.added)
                            painter.setPen(pen)
                            if self.properties.show_text_help:
                                painter.drawText(6, top + height // 1.5, "+")

                        elif diff.startswith("?"):
                            pen.setBrush(self.properties.unknow)
                            painter.setPen(pen)
                            if self.properties.show_text_help:
                                painter.drawText(6, top + height // 1.5, "?")

                        painter.drawLine(
                            point_x,
                            TextEngine(self.editor).point_y_from_line_number(idx),
                            point_x,
                            TextEngine(self.editor).point_y_from_line_number(idx)
                            + height,
                        )
        else:
            with QPainter(self) as painter:
                pen.setBrush(Qt.GlobalColor.darkMagenta)
                painter.setPen(pen)
                if self.properties.show_text_help:
                    painter.drawText(6, top + height // 1.5, "+")

                for _top, block_number, _block in self.editor.visible_blocks:
                    painter.drawLine(
                        point_x,
                        TextEngine(self.editor).point_y_from_line_number(block_number),
                        point_x,
                        TextEngine(self.editor).point_y_from_line_number(block_number)
                        + height,
                    )


__all__ = ["EditionMargin", "EditionMarginWorker"]
