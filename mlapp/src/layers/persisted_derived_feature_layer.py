# -*- coding: utf-8 -*-
from functools import partial

from mlapp.src.layers.features.edits import Edits

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

    def deriveFeatures(self, edits):
        """Retrieve the features in the derived layer and copy them to this layer."""

        # Clean up any instances of the virtual source …
        # self.derivedLayerType.detectAndRemoveAllOfType()
        derivedLayer = self.getDerivedLayerInstance(edits)
        if not derivedLayer:
            raise Glitch(f"{type(self).__name__}.deriveFeatures(): no derived layer to analyse …")

        qgsInfo(f"Deriving {self.name()} …")

        rederiveFeaturesRequest = derivedLayer.getRederiveFeaturesRequest(edits)
        
        edits = Edits()
        if not rederiveFeaturesRequest:
            edits.editBefore(Edits.truncate(self))
        else:
            rederiveFeatures = [f for f in self.getFeatures(rederiveFeaturesRequest)]
            
            qgsDebug(f"rederiveFeaturesRequest.filterExpression={rederiveFeaturesRequest.filterExpression()}")
            
            qgsDebug(f"rederiveFeatures={[str(f) for f in rederiveFeatures]}")
            
            for derivedFeature in rederiveFeatures:
                edits.editBefore(Edits.delete(derivedFeature))

        # Get a second batch of edits that copies the new records to this layer …
        for derivedFeature in derivedLayer.getFeatures():
            edits.editBefore(Edits.upsert(self.copyFeature(derivedFeature)))
        
        return edits
        