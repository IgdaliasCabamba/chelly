from typing import Union
from qtpy.QtGui import QColor, QIcon, QImage
from qtpy.QtCore import QSize, QByteArray, QBuffer
from bs4 import BeautifulSoup

def sanitize_html(value:str, valid_tags:list=["span"]):

    soup = BeautifulSoup(value, features="html.parser")

    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True

    return soup.decode_contents()

def drift_color(base_color, factor=110):
    """
    Return color that is lighter or darker than the base color.
    If base_color.lightness is higher than 128, the returned color is darker
    otherwise is is lighter.
    :param base_color: The base color to drift from
    ;:param factor: drift factor (%)
    :return A lighter or darker color.
    """
    base_color = QColor(base_color)
    if base_color.lightness() > 128:
        return base_color.darker(factor)
    else:
        if base_color == QColor('#000000'):
            return drift_color(QColor('#101010'), factor + 20)
        else:
            return base_color.lighter(factor + 10)

def qimage_to_base64(image:QImage, format: str = "PNG") -> str:
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    image.save(buffer, format)
    return byte_array.toBase64().data().decode("utf-8")

def icon_to_base64(icon: QIcon, size: Union[int, QSize], format: str = "PNG") -> str:
    return qimage_to_base64(icon.pixmap(size).toImage(), format)

def image_to_base64(image:QImage, size: Union[int, QSize], format: str = "PNG") -> str:
    return qimage_to_base64(image.scaled(size), format)