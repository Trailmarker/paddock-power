# -*- coding: utf-8 -*-
from abc import abstractmethod
from .feature_layer import FeatureLayer
from .persisted_layer import PersistedLayer


class PersistedFeatureLayer(FeatureLayer, PersistedLayer):
    @abstractmethod
    def detectInStore(self, storeDefinition, layerName):
        """Detect a matching QgsVectorLayer in a GeoPackage."""
        pass

    @abstractmethod
    def createInStore(self, workspaceFile, layerName):
        """Create a matching QgsVectorLayer in a GeoPackage."""
        pass

    @abstractmethod
    def deleteFromStore(self, workspaceFile, layerName):
        """Delete this layer from the GeoPackage file."""
        pass
    
    @abstractmethod
    def recalculateFeatures(self):
        """Re-derive the upstream features in this layer."""
        pass
    

