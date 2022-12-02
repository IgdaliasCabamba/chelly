from ..core import Feature, TextEngine
from ..internal import chelly_property, ChellyFollowedValue
from qtpy.QtGui import QImage, QPainter
from qtpy.QtCore import QPoint, QSize
from typing import Any, Optional
from typing_extensions import Self

class ImageDrawer(Feature):
    def __init__(self, editor):
        super().__init__(editor)
        self.__qimage_to_paint = None
        self.editor.on_painted.connect(self.paint)
    
    def paint(self, paint_event):
        if not isinstance(self.__qimage_to_paint, QImage):
            return None

        with QPainter(self.editor.viewport()) as painter:
            
            x_offset = self.editor.contentOffset().x()
            viewport_size = self.editor.viewport().size()
            drawable_x = viewport_size.width() - x_offset
            drawable_y = viewport_size.height()

            painter.drawImage(QPoint(0,0), self.__qimage_to_paint.scaled(QSize(drawable_x, drawable_y)))

    @chelly_property
    def draw(self) -> Optional[QImage]:
        return self.__qimage_to_paint
    
    @draw.setter
    def draw(self, qimage:Optional[QImage]):
        self.__qimage_to_paint = qimage
    
    @draw.deleter
    def draw(self):
        self.__qimage_to_paint = None
    
    @draw.follower
    def draw(self, origin:Self, value:Any):
        for editor in self.editor.followers:
            editor_follower_image_drawer = editor.features.get(ImageDrawer)
            if editor_follower_image_drawer is None:
                continue
            editor_follower_image_drawer.draw = ChellyFollowedValue(value)
