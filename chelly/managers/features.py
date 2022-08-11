from inspect import isclass
from ..core.manager import Manager

class FeaturesManager(Manager):
    def __init__(self, editor):
        super().__init__(editor)
        self._features = []
    
    def append(self, feature:object) -> object:
        if callable(feature):
            mode = feature(self.editor)
        else:
            mode = feature
        self._features.append(mode)
        return mode