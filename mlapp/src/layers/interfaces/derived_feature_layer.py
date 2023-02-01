# -*- coding: utf-8 -*-
from abc import abstractproperty
from .feature_layer import FeatureLayer

class DerivedFeatureLayer(FeatureLayer):
    
    @abstractproperty
    def persistedLayers(self):
        """Return the instances of Paddock Power IPersistedLayers used to derive this layer."""
        pass