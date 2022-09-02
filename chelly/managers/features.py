"""
This module allows the ChellyEditor to manage features(functionalities).

Examples:
    >>> from chelly.managers import FeaturesManager
    >>> from chelly.features import IndentationGuides
    >>> editor = ChellyEditor(None)
    >>> editor.features = FeaturesManager

The module contains the following classes:

- `FeaturesManager(editor)` - Create a new FeaturesManager instance with given editor
"""

from ..core.manager import Manager

class FeaturesManager(Manager):
    def __init__(self, editor):
        super().__init__(editor)
        self._features = {}
    
    def append(self, feature:object) -> object:
        """Add the given feature to editor
        
        Examples:
            >>> editor.features.append(CaretLineHighLighter)

        :param feature: the mode to be added to editor.
        :type feature: object

        :returns: the given mode
        :rtype: object
        """

        if callable(feature):
            mode = feature(self.editor)
        else:
            mode = feature

        self._features[mode.__class__.__name__]= mode
        return mode
    
    def get(self, mode):
        """
        Gets a specific feature instance.
        """
        if not isinstance(mode, str):
            mode = mode.__name__
        
        if mode in self._features:
            return self._features[mode]
        
        return None
    
    def remove(self, mode):
        if mode in self._features:
            return self._features[mode]
