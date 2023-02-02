# -*- coding: utf-8 -*-
from abc import abstractmethod
from .persisted_feature_layer import PersistedFeatureLayer


class PersistedDerivedFeatureLayer(PersistedFeatureLayer):

    @property
    @abstractmethod
    def derivedLayer(self):
        """Get the DerivedFeatureLayer from which this layer's features are derived."""
        pass

    @derivedLayer.setter
    def derivedLayer(self, derivedLayer):
        """Set the DerivedFeatureLayer from which this layer's features are derived."""
        pass

    @abstractmethod
    def deriveFeatures(self):
        """Re-derive the upstream features in this layer."""
        pass
    
    def recalculateFeatures(self):
        """We don't do this for derived data, as all values are (or should be) calculated upstream."""
        raise NotImplementedError
