from qtpy.QtGui import QTextBlockUserData


class TextBlockUserData(QTextBlockUserData):
    """
    Custom text block user data, mainly used to store checker messages and
    markers.
    """

    def __init__(self) -> None:
        super().__init__()
        #: List of checker messages associated with the block.
        self.messages = []
        #: List of markers draw by a marker panel.
        self.markers = []


__all__ = ["TextBlockUserData"]
