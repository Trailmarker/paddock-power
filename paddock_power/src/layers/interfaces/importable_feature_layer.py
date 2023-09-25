# -*- coding: utf-8 -*-
from abc import abstractclassmethod, abstractmethod
from .importable_layer import ImportableLayer
from .persisted_feature_layer import PersistedFeatureLayer


class ImportableFeatureLayer(ImportableLayer, PersistedFeatureLayer):

    @abstractmethod
    def makeImportFeatureRequest(self):
        """Return a QgsFeatureRequest with this layer as destination."""
        pass

    @abstractmethod
    def mapFeature(self, importFeature, fieldMap):
        f"""Map a QgsFeature to a Feature."""
        pass

    @abstractmethod
    def importFeatures(self, importLayer, fieldMap):
        """Import all features from the specified layer, applying the given field map."""
        pass

    @abstractclassmethod
    def icon(self):
        """The icon to paint to represent this layer."""
        pass
