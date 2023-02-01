# -*- coding: utf-8 -*-

from ..models import Glitch
from ..utils import PLUGIN_NAME, qgsInfo
from .persisted_feature_layer import PersistedFeatureLayer


class PersistedDerivedFeatureLayer(PersistedFeatureLayer):

    def __init__(self, workspaceFile, layerName, styleName, derivedLayer):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""

        # Ensures that the layer is created in the GeoPackage
        # Adjusts the schema to match the feature type
        # Applies the editor widgets (TODO need to make read only for a derived layer?)
        # Optionally applies a style
        self.derivedLayer = derivedLayer

        super().__init__(workspaceFile, layerName, styleName)
        self.setReadOnly(True)


    def analyseFeatures(self):
        """Analyse the features in the derived layer and copy them to this layer."""
        
        if not self.isEditable():
            raise Glitch(f"{self}.analyseFeatures(): analysis can only be run during an edit session …")
        
        derivedLayer = self.derivedLayer
        if derivedLayer is None:
            raise Glitch(f"{self}.analyseFeatures(): no derived layer to analyse …")
            
        qgsInfo(f"Analysing {self.name()} …")
        self.dataProvider().truncate()

        derivedFeatures = list(derivedLayer.getFeatures())
        for derivedFeature in derivedFeatures:
            feature = self.copyFeature(derivedFeature)
            feature.upsert()