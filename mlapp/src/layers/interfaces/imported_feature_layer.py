# -*- coding: utf-8 -*-
from abc import abstractmethod
from .persisted_feature_layer import PersistedFeatureLayer


class ImportedFeatureLayer(PersistedFeatureLayer):

    @abstractmethod
    def mapFeature(self, importFeature, fieldMap):
        f"""Map a QgsFeature to a Feature."""
        pass

    @abstractmethod
    def importFeatures(self, importLayer, fieldMap):
        """Import all features from the specified layer, applying the given field map."""
        pass