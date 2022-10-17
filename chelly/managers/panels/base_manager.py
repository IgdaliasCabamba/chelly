from typing import Iterator, Union
from dataclasses import dataclass
from ...core import Manager, Panel

class BasePanelManager(Manager):
    
    @dataclass(frozen=True)
    class ZoneSizes:
        left: int
        top: int
        right: int
        bottom: int
    
    def __init__(self, editor) -> None:
        super().__init__(editor)
    
        self._cached_cursor_pos: tuple = (-1, -1)
        self._margin_sizes: tuple = (0, 0, 0, 0)
        self._top: int = -1
        self._left: int = -1
        self._right: int = -1
        self._bottom: int = -1
        self._widgets: dict = {
            Panel.Position.TOP: dict(),
            Panel.Position.LEFT: dict(),
            Panel.Position.RIGHT: dict(),
            Panel.Position.BOTTOM: dict()
        }
        self._zones: list = self._widgets.keys()
        self._settings = dict()
    
    def keys(self) -> list:
        return self._widgets.keys()

    def values(self) -> list:
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

    def panels_located_at_zone(self, zone: Panel.Position) -> list:
        panels_at_zone:dict = self._widgets[zone]
        return list(panels_at_zone.values())

    def zone_where_panel_is_located(self, widget: Union[Panel, str]) -> Union[Panel.Position, None]:
        if not isinstance(widget, str):
            widget = widget.__name__

        for zone in self._zones:
            if widget in self._widgets[zone]:
                return zone

        return None

    def panel_settings(self, widget: Union[Panel, str]) -> Panel.WidgetSettings:
        if not isinstance(widget, str):
            widget = widget.__class__.__name__

        if widget in self._settings.keys():
            return self._settings[widget]

        return Panel.WidgetSettings()
    
    def _valid_panels_at(self, zone: Panel.Position, reverse: bool = False) -> list:
        panels = self.panels_located_at_zone(zone)
        panels.sort(key=lambda panel: panel.order_in_zone, reverse=reverse)
        for panel in panels:
            if not panel.isVisible():
                panels.remove(panel)
        return panels
    
    def _compute_zone_size(self, zone: Panel.Position) -> int:
        res: int = 0
        for panel in self.panels_located_at_zone(zone):
            if panel.isVisible():
                size_hint = panel.sizeHint()
                res += size_hint.width()
        return res
    
    def _viewport_margin(self, zone: Panel.Position) -> int:
        res: int = 0
        for panel in self.panels_located_at_zone(zone):
            if panel.isVisible():
                if zone == Panel.Position.LEFT or zone == Panel.Position.RIGHT:
                    res += panel.sizeHint().width()

                elif zone == Panel.Position.TOP or zone == Panel.Position.BOTTOM:
                    res += panel.sizeHint().height()
        return res
    
    @property
    def zones_sizes(self) -> ZoneSizes:
        """ Compute panel zone sizes """

        self._left = self._compute_zone_size(Panel.Position.LEFT)

        self._right = self._compute_zone_size(Panel.Position.RIGHT)

        self._top = self._compute_zone_size(Panel.Position.TOP)

        self._bottom = self._compute_zone_size(Panel.Position.BOTTOM)

        return BasePanelManager.ZoneSizes(
            left=self._left,
            right=self._right,
            top=self._top,
            bottom=self._bottom
        )
    
    def margin_size(self, zone=Panel.Position.LEFT) -> float:
        return self._margin_sizes[zone]