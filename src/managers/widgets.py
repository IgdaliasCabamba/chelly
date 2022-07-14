from ..core import Manager

class PanelsManager(Manager):
    def __init__(self, editor):
        super().__init__(editor)
        self._widgets = []
    
    def append(self, panel:object) -> object:
        if callable(panel):
            widget = panel(self.editor)
        else:
            widget = panel
        self._widgets.append(widget)
        return widget