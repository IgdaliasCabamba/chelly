from ..core import Manager, Panel, TextFunctions

class PanelsManager(Manager):
    def __init__(self, editor):
        super().__init__(editor)
        
        self._cached_cursor_pos = (-1, -1)
        self._margin_sizes = (0, 0, 0, 0)
        self._top = self._left = self._right = self._bottom = -1
        self._widgets = {
            Panel.Position.TOP: {},
            Panel.Position.LEFT: {},
            Panel.Position.RIGHT: {},
            Panel.Position.BOTTOM: {}
        }

        editor.blockCountChanged.connect(self._update_viewport_margins)
        editor.updateRequest.connect(self._update)
        editor.on_resized.connect(self.refresh)
    
    def append(self, panel:object, position=Panel.Position.LEFT) -> object:
        if callable(panel):
            widget = panel(self.editor)
        else:
            widget = panel

        self._widgets[position][panel.__class__.__name__] = widget
        return widget
    
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

    def keys(self):
        """
        Returns the list of installed panel names.
        """
        return self._widgets.keys()

    def values(self):
        """
        Returns the list of installed panels.
        """
        return self._widgets.values()
    
    def __iter__(self):
        lst = []
        for zone, zone_dict in self._widgets.items():
            for name, panel in zone_dict.items():
                lst.append(panel)
        return iter(lst)

    def __len__(self):
        lst = []
        for zone, zone_dict in self._widgets.items():
            for name, panel in zone_dict.items():
                lst.append(panel)
        return len(lst)

    def panels_for_zone(self, zone):
        """
        Gets the list of panels attached to the specified zone.
        :param zone: Panel position.
        :return: List of panels instances.
        """
        return list(self._widgets[zone].values())

    def refresh(self):
        """ Refreshes the editor panels (resize and update margins) """
        self.resize()
        self._update(self.editor.contentsRect(), 0,
                     force_update_margins=True)

    def resize(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        """ Resizes panels """
        crect = self.editor.contentsRect()
        view_crect = self.editor.viewport().contentsRect()
        s_bottom, s_left, s_right, s_top = self._compute_zones_sizes()
        tw = s_left + s_right
        th = s_bottom + s_top
        w_offset = crect.width() - (view_crect.width() + tw)
        h_offset = crect.height() - (view_crect.height() + th)
        left = 0
        panels = self.panels_for_zone(Panel.Position.LEFT)
        panels.sort(key=lambda panel: panel.order_in_zone, reverse=True)
        for panel in panels:
            if not panel.isVisible():
                continue
            panel.adjustSize()
            size_hint = panel.sizeHint()
            panel.setGeometry(crect.left() + left,
                              crect.top() + s_top,
                              size_hint.width(),
                              crect.height() - s_bottom - s_top - h_offset)
            left += size_hint.width()
        right = 0
        panels = self.panels_for_zone(Panel.Position.RIGHT)
        panels.sort(key=lambda panel: panel.order_in_zone, reverse=True)
        for panel in panels:
            if not panel.isVisible():
                continue
            size_hint = panel.sizeHint()
            panel.setGeometry(
                crect.right() - right - size_hint.width() - w_offset,
                crect.top() + s_top,
                size_hint.width(),
                crect.height() - s_bottom - s_top - h_offset)
            right += size_hint.width()
        top = 0
        panels = self.panels_for_zone(Panel.Position.TOP)
        panels.sort(key=lambda panel: panel.order_in_zone)
        for panel in panels:
            if not panel.isVisible():
                continue
            size_hint = panel.sizeHint()
            panel.setGeometry(crect.left(),
                              crect.top() + top,
                              crect.width() - w_offset,
                              size_hint.height())
            top += size_hint.height()
        bottom = 0
        panels = self.panels_for_zone(Panel.Position.BOTTOM)
        panels.sort(key=lambda panel: panel.order_in_zone)
        for panel in panels:
            if not panel.isVisible():
                continue
            size_hint = panel.sizeHint()
            panel.setGeometry(
                crect.left(),
                crect.bottom() - bottom - size_hint.height() - h_offset,
                crect.width() - w_offset,
                size_hint.height())
            bottom += size_hint.height()

    def _update(self, rect, delta_y, force_update_margins=False):
        """ Updates panels """
        helper = TextFunctions(self.editor)
        if not self:
            return
        
        for zones_id, zone in self._widgets.items():
            if zones_id == Panel.Position.TOP or \
               zones_id == Panel.Position.BOTTOM:
                continue

            panels = list(zone.values())
            for panel in panels:
                
                if panel.scrollable and delta_y:
                    panel.scroll(0, delta_y)

                line, col = helper.cursor_position
                oline, ocol = self._cached_cursor_pos
                
                if line != oline or col != ocol or panel.scrollable:
                    panel.update(0, rect.y(), panel.width(), rect.height())
                self._cached_cursor_pos = helper.cursor_position

        if (rect.contains(self.editor.viewport().rect()) or
                force_update_margins):
            self._update_viewport_margins()

    def _update_viewport_margins(self):
        """ Update viewport margins """
        top = 0
        left = 0
        right = 0
        bottom = 0
        for panel in self.panels_for_zone(Panel.Position.LEFT):
            if panel.isVisible():
                width = panel.sizeHint().width()
                left += width
        for panel in self.panels_for_zone(Panel.Position.RIGHT):
            if panel.isVisible():
                width = panel.sizeHint().width()
                right += width
        for panel in self.panels_for_zone(Panel.Position.TOP):
            if panel.isVisible():
                height = panel.sizeHint().height()
                top += height
        for panel in self.panels_for_zone(Panel.Position.BOTTOM):
            if panel.isVisible():
                height = panel.sizeHint().height()
                bottom += height
        self._margin_sizes = (top, left, right, bottom)
        self.editor.setViewportMargins(left, top, right, bottom)

    def margin_size(self, position=Panel.Position.LEFT):
        """
        Gets the size of a specific margin.
        :param position: Margin position. See
            :class:`pyqode.core.api.Panel.Position`
        :return: The size of the specified margin
        :rtype: float
        """
        return self._margin_sizes[position]

    def _compute_zones_sizes(self):
        """ Compute panel zone sizes """
        # Left panels
        left = 0
        for panel in self.panels_for_zone(Panel.Position.LEFT):
            if not panel.isVisible():
                continue
            size_hint = panel.sizeHint()
            left += size_hint.width()
        # Right panels
        right = 0
        for panel in self.panels_for_zone(Panel.Position.RIGHT):
            if not panel.isVisible():
                continue
            size_hint = panel.sizeHint()
            right += size_hint.width()
        # Top panels
        top = 0
        for panel in self.panels_for_zone(Panel.Position.TOP):
            if not panel.isVisible():
                continue
            size_hint = panel.sizeHint()
            top += size_hint.height()
        # Bottom panels
        bottom = 0
        for panel in self.panels_for_zone(Panel.Position.BOTTOM):
            if not panel.isVisible():
                continue
            size_hint = panel.sizeHint()
            bottom += size_hint.height()

        self._top, self._left, self._right, self._bottom = (
            top, left, right, bottom)
        return bottom, left, right, top