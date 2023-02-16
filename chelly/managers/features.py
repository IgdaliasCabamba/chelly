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

from typing import Dict, List
from typing_extensions import Self
from ..core.dev import Manager
from ..core import Feature


class FeaturesManager(Manager):
    def __init__(self, editor):
        super().__init__(editor)
        self._features: Dict[str, Feature] = {}

    def append(self, feature: Feature) -> Feature:
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

        self._features[mode.__class__.__name__] = mode
        return mode

    def get(self, mode: Feature):
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

    @property
    def as_list(self) -> List[Feature]:
        return self._features.values()

    def __shared_reference(self, other_manager: Self) -> Self:
        for from_feature in other_manager.as_list:
            to_feature = self.get(from_feature.__class__)
            if to_feature is not None:
                to_feature.shared_reference = from_feature.shared_reference

    shared_reference = property(fset=__shared_reference)
    del __shared_reference


__all__ = ["FeaturesManager"]
