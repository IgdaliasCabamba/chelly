from ...core import Panel, TextEngine
from qtpy.QtCore import QRect, QSize
from .base_manager import BasePanelManager

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