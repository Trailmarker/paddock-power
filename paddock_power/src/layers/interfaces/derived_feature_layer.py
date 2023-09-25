# -*- coding: utf-8 -*-
from abc import abstractmethod
from .feature_layer import FeatureLayer


class DerivedFeatureLayer(FeatureLayer):

    @property
    @abstractmethod
    def persistedLayers(self):
        """Return the instances of Paddock Power IPersistedLayers used to derive this layer."""
        pass
