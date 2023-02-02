# -*- coding: utf-8 -*-

from ..models import Glitch
from ..utils import PLUGIN_NAME, qgsInfo
from .interfaces import IPersistedDerivedFeatureLayer
from .persisted_feature_layer import PersistedFeatureLayer

class PersistedDerivedFeatureLayer(PersistedFeatureLayer, IPersistedDerivedFeatureLayer):

    def __init__(self, workspaceFile, layerName, styleName, derivedLayer):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""
        self._derivedLayer = derivedLayer

        super().__init__(workspaceFile, layerName, styleName)

        self.setReadOnly(True)

    @property
    def derivedLayer(self):
        """Get the DerivedFeatureLayer from which this layer's features are derived."""
        return self._derivedLayer

    @derivedLayer.setter
    def derivedLayer(self, derivedLayer):
        """Set the DerivedFeatureLayer from which this layer's features are derived."""
        self._derivedLayer = derivedLayer

    def deriveFeatures(self):
        """Retrieve the features in the derived layer and copy them to this layer."""

        if not self.isEditable():
            raise Glitch(f"{type(self).__name__}.deriveFeatures(): this can only be run during an edit session …")

        derivedLayer = self.derivedLayer
        if not derivedLayer:
            raise Glitch(f"{type(self).__name__}.deriveFeatures(): no derived layer to analyse …")

        qgsInfo(f"Deriving {self.name()} …")
        self.dataProvider().truncate()

        derivedFeatures = list(derivedLayer.getFeatures())
        for derivedFeature in derivedFeatures:
            feature = self.copyFeature(derivedFeature)
            feature.upsert()
