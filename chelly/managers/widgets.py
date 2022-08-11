from typing import Iterator, Union
from dataclasses import dataclass
from ..core import Manager, Panel, TextEngine
from PySide6.QtCore import QRect


class PanelsManager(Manager):

    @dataclass(frozen=True)
    class ZoneSizes:
        left: int
        top: int
        right: int
        bottom: int

    def __init__(self, editor) -> None:
        super().__init__(editor)

        self._cached_cursor_pos:tuple = (-1, -1)
        self._margin_sizes:tuple = (0, 0, 0, 0)
        self._top:int = -1
        self._left:int = -1
        self._right:int = -1
        self._bottom:int = -1
        self._widgets:dict = {
            Panel.Position.TOP: {},
            Panel.Position.LEFT: {},
            Panel.Position.RIGHT: {},
            Panel.Position.BOTTOM: {}
        }
        self._zones:list = self._widgets.keys()

        self.editor.blockCountChanged[int].connect(
            self._update_viewport_margins)
        self.editor.updateRequest[QRect, int].connect(self._update)
        self.editor.on_resized.connect(self.refresh)

    def append(self, panel: Panel, position=Panel.Position.LEFT) -> Panel:
        if callable(panel):
            widget = panel(self.editor)
        else:
            widget = panel

        self._widgets[position][panel.__class__.__name__] = widget
        return widget
    
    def remove(self, panel: Panel) -> None:
        pass

    def get(self, widget):
        """
        Gets a specific panel instance.
        """
        if not isinstance(widget, str):
            widget = widget.__name__

        for zone in range(4):
            try:
                return self._widgets[zone][widget]
            except KeyError:
                return None

    def keys(self) -> list:
        """
        Returns the list of installed panel names.
        """
        return self._widgets.keys()

    def values(self) -> list:
        """
        Returns the list of installed panels.
        """
        return self._widgets.values()

    def __iter__(self) -> Iterator:
        lst = []
        for zone, zone_dict in self._widgets.items():
            for name, panel in zone_dict.items():
                lst.append(panel)
        return iter(lst)

    def __len__(self) -> int:
        lst = []
        for zone, zone_dict in self._widgets.items():
            for name, panel in zone_dict.items():
                lst.append(panel)
        return len(lst)

    def panels_for_zone(self, zone: Panel.Position) -> list:
        """
        Gets the list of panels attached to the specified zone.
        :param zone: Panel position.
        :return: List of panels instances.
        """
        return list(self._widgets[zone].values())

    def panel_zone(self, widget: Union[Panel, str]) -> Union[Panel.Position, None]:
        if not isinstance(widget, str):
            widget = widget.__name__

        for zone in self._zones:
            if widget in self._widgets[zone]:
                return zone

        return None

    def refresh(self) -> None:
        """ Refreshes the editor panels (resize and update margins) """
        self.resize()
        self._update(self.editor.contentsRect(), 0,
                     force_update_margins=True)

    def _valid_panels_at(self, zone: Panel.Position, reverse: bool = False) -> list:
        panels = self.panels_for_zone(zone)
        panels.sort(key=lambda panel: panel.order_in_zone, reverse=reverse)
        for panel in panels:
            if not panel.isVisible():
                panels.remove(panel)
        return panels

    def resize(self) -> None:
        """ Resizes panels """
        crect = self.editor.contentsRect()
        view_crect = self.editor.viewport().contentsRect()
        zones_sizes = self.zones_sizes

        size_top = zones_sizes.top
        size_bottom = zones_sizes.bottom
        size_right = zones_sizes.right
        size_left = zones_sizes.left

        tw = size_left + size_right
        th = size_bottom + size_top
        w_offset = crect.width() - (view_crect.width() + tw)
        h_offset = crect.height() - (view_crect.height() + th)

        left: int = 0
        for panel in self._valid_panels_at(Panel.Position.LEFT, True):
            panel.adjustSize()
            size_hint = panel.sizeHint()
            panel.setGeometry(crect.left() + left,
                              crect.top() + size_top,
                              size_hint.width(),
                              crect.height() - size_bottom - size_top - h_offset)
            left += size_hint.width()

        right: int = 0
        for panel in self._valid_panels_at(Panel.Position.RIGHT, True):
            size_hint = panel.sizeHint()
            panel.setGeometry(
                crect.right() - right - size_hint.width() - w_offset,
                crect.top() + size_top,
                size_hint.width(),
                crect.height() - size_bottom - size_top - h_offset)
            right += size_hint.width()

        top: int = 0
        for panel in self._valid_panels_at(Panel.Position.TOP):
            size_hint = panel.sizeHint()
            panel.setGeometry(crect.left(),
                              crect.top() + top,
                              crect.width() - w_offset,
                              size_hint.height())
            top += size_hint.height()

        bottom: int = 0
        for panel in self._valid_panels_at(Panel.Position.BOTTOM):
            size_hint = panel.sizeHint()
            panel.setGeometry(
                crect.left(),
                crect.bottom() - bottom - size_hint.height() - h_offset,
                crect.width() - w_offset,
                size_hint.height())
            bottom += size_hint.height()

    def _update(self, rect:object, delta_y:int, force_update_margins:bool=False) -> None:
        """ Updates panels """
        helper = TextEngine(self.editor)

        for zones_id, zone in self._widgets.items():
            if zones_id == Panel.Position.TOP or zones_id == Panel.Position.BOTTOM:
                continue

            panels = list(zone.values())
            for panel in panels:

                if panel.scrollable and delta_y:
                    panel.scroll(0, delta_y)

                line, col = helper.cursor_position
                cached_line, cached_column = self._cached_cursor_pos

                if line != cached_line or col != cached_column or panel.scrollable:
                    panel.update(0, rect.y(), panel.width(), rect.height())
                self._cached_cursor_pos = helper.cursor_position

        if (rect.contains(self.editor.viewport().rect()) or
                force_update_margins):
            self._update_viewport_margins()

    def _viewport_margin(self, zone: Panel.Position) -> int:
        res: int = 0
        for panel in self.panels_for_zone(zone):
            if panel.isVisible():
                if zone == Panel.Position.LEFT or zone == Panel.Position.RIGHT:
                    res += panel.sizeHint().width()

                elif zone == Panel.Position.TOP or zone == Panel.Position.BOTTOM:
                    res += panel.sizeHint().height()
        return res

    def _update_viewport_margins(self) -> None:
        """ Update viewport margins """
        top = self._viewport_margin(Panel.Position.TOP)
        left = self._viewport_margin(Panel.Position.LEFT)
        right = self._viewport_margin(Panel.Position.RIGHT)
        bottom = self._viewport_margin(Panel.Position.BOTTOM)

        self._margin_sizes = (top, left, right, bottom)
        self.editor.setViewportMargins(left, top, right, bottom)  # pattern

    def margin_size(self, zone=Panel.Position.LEFT) -> float:
        return self._margin_sizes[zone]

    def _compute_zone_size(self, zone: Panel.Position) -> int:
        res: int = 0
        for panel in self.panels_for_zone(zone):
            if panel.isVisible():
                size_hint = panel.sizeHint()
                res += size_hint.width()
        return res

    @property
    def zones_sizes(self) -> ZoneSizes:
        """ Compute panel zone sizes """

        self._left = self._compute_zone_size(Panel.Position.LEFT)

        self._right = self._compute_zone_size(Panel.Position.RIGHT)

        self._top = self._compute_zone_size(Panel.Position.TOP)

        self._bottom = self._compute_zone_size(Panel.Position.BOTTOM)

        return PanelsManager.ZoneSizes(
            left=self._left,
            right=self._right,
            top=self._top,
            bottom=self._bottom
        )
