# -*- coding: utf-8 -*-
from functools import partial

from ..models import Glitch
from ..utils import PLUGIN_NAME, qgsDebug, qgsInfo
from .interfaces import IPersistedDerivedFeatureLayer
from .persisted_feature_layer import PersistedFeatureLayer


class PersistedDerivedFeatureLayer(PersistedFeatureLayer, IPersistedDerivedFeatureLayer):

    def __init__(self, workspaceFile, layerName, styleName, derivedLayerType, dependentLayers):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""
        super().__init__(workspaceFile, layerName, styleName)

        self.derivedLayerType = derivedLayerType
        self.dependentLayers = dependentLayers
        
        self.setReadOnly(True)

    def getDerivedLayerInstance(self, edits):
        """Return the derived layer for this layer."""
        return self.derivedLayerType(self.dependentLayers, edits)

    def showDerivedLayerInstance(self):
        """Add an instance of the derived layer for this layer to the map."""
        self.getDerivedLayerInstance(edits=None).addToMap()

    def deriveFeatures(self, edits, featureProgressCallback=None, cancelledCallback=None):
        """Retrieve the features in the derived layer and copy them to this layer."""

        # Clean up any instances of the virtual source …
        # self.derivedLayerType.detectAndRemoveAllOfType()

        if not self.isEditable():
            raise Glitch(f"{type(self).__name__}.deriveFeatures(): this can only be run during an edit session …")

        derivedLayer = self.getDerivedLayerInstance(edits)
        if not derivedLayer:
            raise Glitch(f"{type(self).__name__}.deriveFeatures(): no derived layer to analyse …")

        qgsInfo(f"Deriving {self.name()} …")
       
        # Remove features based on the edits that have been applied upstream …
        derivedLayer.cleanDerivedFeatures(self, edits)

        derivedFeatures = list(derivedLayer.getFeatures())

        featureCount = len(derivedFeatures)
        count = 0

        for derivedFeature in derivedFeatures:
            if cancelledCallback and cancelledCallback():
                return
            feature = self.copyFeature(derivedFeature)
            feature.upsert()
            if featureProgressCallback:
                featureProgressCallback(count, featureCount)

        # Check again …
        if cancelledCallback and cancelledCallback():
            return

        # Clean up any instances of the virtual source …
        # type(derivedLayer).detectAndRemoveAllOfType()
