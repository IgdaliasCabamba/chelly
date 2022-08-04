from PySide6.QtCore import QObject, Signal

class Manager(QObject):
    
    on_state_changed = Signal(object)

    def __init__(self, editor):
        super().__init__()
        self.__editor = editor
    
    @property
    def editor(self):
        return self.__editor
    
