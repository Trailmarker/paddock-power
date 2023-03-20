# -*- coding: utf-8 -*-
from abc import abstractclassmethod, abstractmethod
from .persisted_feature_layer import PersistedFeatureLayer


class ImportableFeatureLayer(PersistedFeatureLayer):

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
    
