from ..core import Feature, TextEngine
from ..internal import chelly_imitable
from qtpy.QtGui import QImage, QPainter
from qtpy.QtCore import QPoint, QSize

class ImageDrawer(Feature):
    def __init__(self, editor):
        super().__init__(editor)
        self.__to_paint = None
        self.editor.on_painted.connect(self.paint)
    
    def paint(self, paint_event):
        if not isinstance(self.__to_paint, QImage):
            return None

        with QPainter(self.editor.viewport()) as painter:
            
            x_offset = self.editor.contentOffset().x()
            viewport_size = self.editor.viewport().size()
            drawable_x = viewport_size.width() - x_offset
            drawable_y = viewport_size.height()

            painter.drawImage(QPoint(0,0), self.__to_paint.scaled(QSize(drawable_x, drawable_y)))

    @chelly_imitable
    def draw(self):
        return self.__to_paint
    
    @draw.setter
    def draw(self, qimage:QImage):
        self.__to_paint = qimage
    
    @draw.deleter
    def draw(self):
        self.__to_paint = None
