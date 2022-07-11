from ..core import Manager

class PanelsManager(Manager):
    def __init__(self, parent):
        self.editor = parent
        self._widgets = []
    
    def add(self, panel:object) -> object:
        if callable(panel):
            widget = panel(self.editor)
        else:
            widget = panel
        self._widgets.append(widget)
        return widget