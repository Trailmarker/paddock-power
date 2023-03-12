# -*- coding: utf-8 -*-
from abc import abstractmethod
from .persisted_feature_layer import PersistedFeatureLayer


class PersistedDerivedFeatureLayer(PersistedFeatureLayer):

    @abstractmethod
    def deriveFeatures(self, changeset=None):
        """Re-derive the upstream features in this layer."""
        pass

    def recalculateFeatures(self):
        """We don't do this for derived data, as all values are (or should be) calculated upstream."""
        raise NotImplementedError
