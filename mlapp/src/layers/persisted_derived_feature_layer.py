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

    def getDerivedLayerInstance(self, changeset=None):
        """Return the derived layer for this layer."""
        return self.derivedLayerType(self.dependentLayers, changeset)

    def showDerivedLayerInstance(self, changeset=None):
        """Add an instance of the derived layer for this layer to the map."""
        self.getDerivedLayerInstance(changeset).addToMap()

    def deriveFeatures(self, changeset):
        """Retrieve the features in the derived layer and copy them to this layer."""

        # Clean up any instances of the virtual source …
        # self.derivedLayerType.detectAndRemoveAllOfType()
        derivedLayer = self.getDerivedLayerInstance(changeset)
        if not derivedLayer:
            raise Glitch(f"{type(self).__name__}.deriveFeatures(): no derived layer to analyse …")

        rederiveFeaturesRequest = derivedLayer.getRederiveFeaturesRequest()
        
        edits = Edits()
        if not rederiveFeaturesRequest:
            qgsInfo(f"Removing and re-deriving the whole {self.name()} layer …")
            edits.editBefore(Edits.truncate(self))
        else:
            rederivedFeatures = [f for f in self.getFeatures(rederiveFeaturesRequest)]
            qgsInfo(f"Removing {len(rederivedFeatures)} features in the {self.name()} layer …")
            
            for rederivedFeature in rederivedFeatures:
                edits.editBefore(Edits.delete(rederivedFeature))

        derivedFeatures = [self.copyFeature(f) for f in derivedLayer.getFeatures()] 
        qgsInfo(f"Deriving {len(derivedFeatures)} features in the {self.name()} layer …")
        
        # Get a second batch of edits that copies the new records to this layer …
        edits.editBefore(Edits.bulkAdd({
            'layer': self,
            'features': derivedFeatures
            }))
        
        # for derivedFeature in derivedFeatures:
        #     edits.editBefore(Edits.upsert(self.copyFeature(derivedFeature)))
        
        return edits
        