from PySide6.QtGui import QColor
from bs4 import BeautifulSoup

VALID_TAGS = ["span"]


def sanitize_html(value:str):

    soup = BeautifulSoup(value, features="html.parser")

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
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