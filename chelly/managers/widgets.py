from typing import Iterator, Union
from dataclasses import dataclass
from typing_extensions import Self
from ..core import Manager, Panel, TextEngine
from qtpy.QtCore import QRect, QSize

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

    def panel_settings(self, widget: Union[Panel, str]) -> Panel.Settings:
        if not isinstance(widget, str):
            widget = widget.__class__.__name__

        if widget in self._settings.keys():
            return self._settings[widget]

        return Panel.Settings()
    
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

class PanelsSizeHelpers(BasePanelManager):
    def __init__(self, editor) -> None:
        super().__init__(editor)
    
    def resize_left(self,
        contents_rect:QRect,
        zone_sizes:BasePanelManager.ZoneSizes,
        heigth_offset:int
        ) -> int:

        left_size = 0
        for panel in self._valid_panels_at(Panel.Position.LEFT, True):
            panel.adjustSize()
            size_hint: QSize = panel.sizeHint()
            
            x = contents_rect.left() + left_size
            y = contents_rect.top() + zone_sizes.top
            w = size_hint.width()
            h = contents_rect.height() - zone_sizes.bottom - zone_sizes.top - heigth_offset

            level = self.panel_settings(panel).level
            
            if level == 1:
                h = contents_rect.height() - zone_sizes.top - heigth_offset

            elif level == 2:
                h = contents_rect.height() - heigth_offset
            
            panel.setGeometry(x,y,w,h)
            left_size += size_hint.width()

        return left_size
    
    def resize_right(self,
        contents_rect:QRect,
        zone_sizes:BasePanelManager.ZoneSizes,
        width_offset:int,
        heigth_offset:int,
        ) -> int:

        rigth_size = 0
        for panel in self._valid_panels_at(Panel.Position.RIGHT, True):
            size_hint: QSize = panel.sizeHint()

            x = contents_rect.right() - rigth_size - size_hint.width() - width_offset
            y = contents_rect.top() + zone_sizes.top
            w = size_hint.width()
            h = contents_rect.height() -  zone_sizes.bottom - zone_sizes.top - heigth_offset

            index = self.panel_settings(panel).level

            if index == 1:
                h = contents_rect.height() - zone_sizes.top - heigth_offset

            elif index == 2:
                h = contents_rect.height() - heigth_offset
            
            panel.setGeometry(x,y,w,h)

            rigth_size += size_hint.width()

        return rigth_size
    
    def resize_top(self,
        contents_rect:QRect,
        width_offset:int,
        right_size:int,
        ) -> int:

        top_size = 0
        for panel in self._valid_panels_at(Panel.Position.TOP):
            size_hint: QSize = panel.sizeHint()

            index = self.panel_settings(panel).level

            x = contents_rect.left()
            y = contents_rect.top() + top_size
            w = contents_rect.width() - width_offset - right_size
            h = size_hint.height()

            if index == 1:
                w = contents_rect.width() - width_offset
                
            elif index == 2:
                w = contents_rect.width()
                
            panel.setGeometry(x,y,w,h)
            top_size += size_hint.height()

        return top_size
    
    def resize_bottom(self,
        contents_rect:QRect,
        width_offset:int,
        heigth_offset:int,
        right_size:int,
        ) -> int:

        bottom_size = 0
        for panel in self._valid_panels_at(Panel.Position.BOTTOM):
            size_hint: QSize = panel.sizeHint()

            x = contents_rect.left()
            y = contents_rect.bottom() - bottom_size - size_hint.height() - heigth_offset
            w = contents_rect.width() - width_offset - right_size
            h = size_hint.height()

            index = self.panel_settings(panel).level

            if index == 1:
                w = contents_rect.width() - width_offset

            elif index == 2:
                w = contents_rect.width()

            panel.setGeometry(x, y, w, h)
            bottom_size += size_hint.height()

        return bottom_size


    
    def resize(self) -> None:
        """ Resizes panels """
        contents_rect = self.editor.contentsRect()
        view_contents_rect = self.editor.viewport().contentsRect()
        zones_sizes = self.zones_sizes

        total_width = zones_sizes.left + zones_sizes.right
        total_height = zones_sizes.bottom + zones_sizes.top
        width_offset = contents_rect.width() - (view_contents_rect.width() + total_width)
        heigth_offset = contents_rect.height() - (view_contents_rect.height() + total_height)

        left_size = self.resize_left(contents_rect, zones_sizes, heigth_offset)
        right_size = self.resize_right(contents_rect, zones_sizes, width_offset, heigth_offset)
        top_size = self.resize_top(contents_rect, width_offset, right_size)
        bottom_size = self.resize_bottom(contents_rect, width_offset, heigth_offset, right_size)

class PanelsManager(PanelsSizeHelpers):
    
    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.bind()

    def bind(self):
        self.editor.blockCountChanged[int].connect(self.update_viewport_margins)
        self.editor.updateRequest[QRect, int].connect(self.update)
        self.editor.on_resized.connect(self.refresh)
    
    def _call_panel(self, panel: Panel) -> Union[None, Panel]:
        if callable(panel):
            # avoid appending more than one of the same panel type
            if self.get(panel.__name__):
                return None
            widget = panel(self.editor)
        else:
            # avoid appending more than one of the same panel type
            if self.get(panel.__class__.__name__):
                return None
            widget = panel
        return widget

    def append(self, panel: Panel, zone=Panel.Position.LEFT, settings = Panel.Settings()) -> Panel:
        widget = self._call_panel(panel)

        if widget is not None:
            widget_name = widget.__class__.__name__
            self._widgets[zone][widget_name] = widget
            self._settings[widget_name] = settings
            return widget

        # make it like a singleton
        if callable(panel):
            return self.get(panel.__name__)

        return self.get(panel.__class__.__name__)

    def remove(self, panel: Panel) -> Self:
        if not isinstance(panel, str):
            widget_name = panel.__name__
        
        for zone in Panel.Position.iterable():
            try:
                self._widgets[zone].pop(widget_name)
                self._settings.pop(widget_name)
                return self

            except KeyError:
                pass
        
        return self

    def get(self, widget):
        """
        Gets a specific panel instance.
        """
        if not isinstance(widget, str):
            widget = widget.__name__

        for zone in Panel.Position.iterable():
            try:
                return self._widgets[zone][widget]
            except KeyError:
                pass
        return None

    def refresh(self) -> None:
        """ Refreshes the editor panels (resize and update margins) """
        self.resize()
        self.update(self.editor.contentsRect(), 0,
                     force_update_margins=True)

    def update(self, rect: object, delta_y: int, force_update_margins: bool = False) -> None:
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
            self.update_viewport_margins()

    def update_viewport_margins(self) -> None:
        """ Update viewport margins """
        top = self._viewport_margin(Panel.Position.TOP)
        left = self._viewport_margin(Panel.Position.LEFT)
        right = self._viewport_margin(Panel.Position.RIGHT)
        bottom = self._viewport_margin(Panel.Position.BOTTOM)

        self._margin_sizes = (top, left, right, bottom)
        self.editor.setViewportMargins(left, top, right, bottom)  # pattern