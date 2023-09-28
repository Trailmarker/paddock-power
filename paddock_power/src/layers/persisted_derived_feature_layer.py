# -*- coding: utf-8 -*-
from ..layers.features import Edits
from ..models import Glitch
from ..utils import PLUGIN_NAME, getSetting, qgsInfo
from .interfaces import IPersistedDerivedFeatureLayer
from .persisted_feature_layer import PersistedFeatureLayer


class PersistedDerivedFeatureLayer(PersistedFeatureLayer, IPersistedDerivedFeatureLayer):

    RESPECT_CHANGESETS = getSetting("respectChangesets", default=False)

    def __init__(self, workspaceFile, layerName, styleName, derivedLayerType, dependentLayers):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""
        super().__init__(workspaceFile, layerName, styleName)

        self.derivedLayerType = derivedLayerType
        self.dependentLayers = dependentLayers

        self.setReadOnly(True)

    def getDerivedLayer(self, changeset=None):
        """Return the derived layer for this layer."""
        # Clean up any instances of the virtual source …
        self.derivedLayerType.removeAllOfType()

        # Create the new instance and return
        return self.derivedLayerType(self.dependentLayers, changeset)

    def showDerivedLayer(self, changeset=None):
        """Add an instance of the derived layer for this layer to the map."""
        self.getDerivedLayer(changeset).addToMap()

    def deriveFeatures(self, changeset=None, raiseErrorIfTaskHasBeenCancelled=lambda: None):
        """Retrieve the features in the derived layer and copy them to this layer."""

        # RESPECT_CHANGESETS determines whether we try to home in just on dependent data
        derivedLayer = self.getDerivedLayer(
            changeset) if self.RESPECT_CHANGESETS else self.getDerivedLayer(None)
        if not derivedLayer:
            raise Glitch(f"{type(self).__name__}.deriveFeatures(): no derived layer to analyse …")

        raiseErrorIfTaskHasBeenCancelled()

        rederiveFeaturesRequest = derivedLayer.getRederiveFeaturesRequest() if self.RESPECT_CHANGESETS else None

        raiseErrorIfTaskHasBeenCancelled()

        edits = Edits()
        if not rederiveFeaturesRequest:
            qgsInfo(f"Removing and re-deriving the whole {self.name()} layer …")
            edits.editBefore(Edits.truncate(self))
        else:
            rederivedFeatures = [f for f in self.getFeatures(rederiveFeaturesRequest)]
            qgsInfo(f"Removing {len(rederivedFeatures)} features in the {self.name()} layer …")

            raiseErrorIfTaskHasBeenCancelled()

            for rederivedFeature in rederivedFeatures:
                edits.editBefore(Edits.delete(rederivedFeature))

        derivedFeatures = []

        for f in derivedLayer.getFeatures():
            raiseErrorIfTaskHasBeenCancelled()
            derivedFeatures.append(self.copyFeature(f))

        qgsInfo(f"Deriving {len(derivedFeatures)} features in the {self.name()} layer …")

        # Get a second batch of edits that copies the new records to this layer …
        edits.editBefore(Edits.bulkAdd(self, derivedFeatures))

        # Clean up the derived layer after all this gets persisted
        edits.editBefore(Edits.cleanupDerivedLayer(self, derivedLayer))

        # Get rid of the derived layer … does not work
        # QgsProject.instance().removeMapLayer(derivedLayer.id())
        return edits
