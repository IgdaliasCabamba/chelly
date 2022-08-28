from PySide6.QtWidgets import QWidget

class Panel(QWidget):

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.order_in_zone = -1
        self._scrollable = False
        self.__enabled = True
        self.__editor = editor
        self.editor.panels.refresh()

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, status:bool) -> None:
        self.__enabled = status
        
    @property
    def editor(self):
        return self.__editor
    
    @property
    def scrollable(self) -> bool:
        """
        A scrollable panel will follow the editor's scroll-bars. Left and right
        panels follow the vertical scrollbar. Top and bottom panels follow the
        horizontal scrollbar.
        :type: bool
        """
        return self._scrollable

    @scrollable.setter
    def scrollable(self, value:bool):
        self._scrollable = value


    class Position(object):
        """
        Enumerates the possible panel positions
        """
        #: Top margin
        TOP = 0
        #: Left margin
        LEFT = 1
        #: Right margin
        RIGHT = 2
        #: Bottom margin
        BOTTOM = 3

        @classmethod
        def iterable(cls):
            """ Returns possible positions as an iterable (list) """
            return [cls.TOP, cls.LEFT, cls.RIGHT, cls.BOTTOM]

    def setVisible(self, visible:bool):
        """
        Shows/Hides the panel
        Automatically call CodeEdit.refresh_panels.
        :param visible: Visible state
        """
        super().setVisible(visible)
        if self.editor:
            self.editor.panels.refresh()
    
    @property
    def fixed_size_hint(self):
        return 0