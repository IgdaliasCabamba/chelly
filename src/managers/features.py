from inspect import isclass
from ..core.manager import Manager

class FeaturesManager(Manager):
    def __init__(self, parent):
        self.editor = parent
        self._features = []
    
    def add(self, feature:object) -> object:
        if callable(feature):
            mode = feature(self.editor)
        else:
            mode = feature
        self._features.append(mode)
        return mode