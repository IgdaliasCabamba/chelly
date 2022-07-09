from PySide6.QtWidgets import QWidget

class MarginManager(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor = parent
        self._components = {}
    
    @property
    def components(self) -> dict:
        return self._components
    
    def append(self, component, name:str = None) -> object:
        component_instance = component(self.editor)

        if name is not None:
            self._components[name] = component_instance
        else:
            self._components[component] = component_instance
        
        return component_instance