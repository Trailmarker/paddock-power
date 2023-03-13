# -*- coding: utf-8 -*-
from ..layers.features import Edits
from ..models import Glitch
from ..utils import PLUGIN_NAME, qgsInfo
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
        self.derivedLayerType.removeAllOfType()
        return self.derivedLayerType(self.dependentLayers, changeset)

    def showDerivedLayerInstance(self, changeset=None):
        """Add an instance of the derived layer for this layer to the map."""
        self.getDerivedLayerInstance(changeset).addToMap()

    def deriveFeatures(self, changeset=None, RAISE_IF_CANCELLED=None):
        """Retrieve the features in the derived layer and copy them to this layer."""

        # Clean up any instances of the virtual source …
        derivedLayer = self.getDerivedLayerInstance(changeset)
        if not derivedLayer:
            raise Glitch(f"{type(self).__name__}.deriveFeatures(): no derived layer to analyse …")

        RAISE_IF_CANCELLED()

        rederiveFeaturesRequest = derivedLayer.getRederiveFeaturesRequest()

        RAISE_IF_CANCELLED()

        edits = Edits()
        if not rederiveFeaturesRequest:
            qgsInfo(f"Removing and re-deriving the whole {self.name()} layer …")
            edits.editBefore(Edits.truncate(self))
        else:
            rederivedFeatures = [f for f in self.getFeatures(rederiveFeaturesRequest)]
            qgsInfo(f"Removing {len(rederivedFeatures)} features in the {self.name()} layer …")

            RAISE_IF_CANCELLED()

            for rederivedFeature in rederivedFeatures:
                edits.editBefore(Edits.delete(rederivedFeature))

        derivedFeatures = []
        
        for f in derivedLayer.getFeatures():
            RAISE_IF_CANCELLED()
            derivedFeatures.append(self.copyFeature(f))

        qgsInfo(f"Deriving {len(derivedFeatures)} features in the {self.name()} layer …")

        # Get a second batch of edits that copies the new records to this layer …
        edits.editBefore(Edits.bulkAdd(self, derivedFeatures))

        # Get rid of the derived layer … does not work
        # QgsProject.instance().removeMapLayer(derivedLayer.id())
        return edits

