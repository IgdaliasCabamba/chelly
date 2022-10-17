from typing import Union, List
from typing_extensions import Self
from ...core import Panel, TextEngine
from qtpy.QtCore import QRect
from .size_helpers import PanelsSizeHelpers

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

    def append(self, panel: Panel, zone=Panel.Position.LEFT, settings = Panel.WidgetSettings()) -> Panel:
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

    def get(self, widget) -> Panel:
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
    
    @property
    def as_list(self) -> List[Panel]:
        return list(self)
    
    def __shared_reference(self, other_manager:Self) -> Self:
        for from_feature in other_manager.as_list:
            to_feature = self.get(from_feature.__class__)
            if to_feature is not None:
                to_feature.shared_reference = from_feature.shared_reference
    
    shared_reference = property(fset=__shared_reference)
    del __shared_reference