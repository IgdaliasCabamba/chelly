from PySide6.QtGui import QColor

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