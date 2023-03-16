# -*- coding: utf-8 -*-
from abc import abstractmethod
from .feature_layer import FeatureLayer
from .persisted_layer import PersistedLayer


class PersistedFeatureLayer(FeatureLayer, PersistedLayer):
    @classmethod
    def workspaceUrl(cls, workspaceFile):
        """Return the expected GeoPackage URL for this layer for a given workspace GeoPackage."""
        return f"{workspaceFile}|layername={cls.defaultName()}"

    @abstractmethod
    def detectInStore(self, workspaceFile, layerName):
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
    def recalculateFeatures(self, raiseErrorIfTaskHasBeenCancelled=lambda: None):
        """Re-derive the upstream features in this layer."""
        pass
