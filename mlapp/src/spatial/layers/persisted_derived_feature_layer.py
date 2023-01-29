# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from ...utils import PLUGIN_NAME, qgsInfo
from .persisted_feature_layer import PersistedFeatureLayer
from ..features.edits import Edits


class PersistedDerivedFeatureLayer(PersistedFeatureLayer):

    def __init__(self, featureType, workspaceFile, layerName, styleName, derivedLayer):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""

        # Ensures that the layer is created in the GeoPackage
        # Adjusts the schema to match the feature type
        # Applies the editor widgets (TODO need to make read only for a derived layer?)
        # Optionally applies a style
        self.derivedLayer = derivedLayer
        
        super().__init__(featureType, workspaceFile, layerName, styleName)
        self.setReadOnly(True)  # TODO?
        
        # Initial persistence
        # self.repersistDerivedFeatures(None, [])
  

    @pyqtSlot()
    def repersistDerivedFeatures(self, layer, idList):
        """Derive all Features to be persisted from the source DerivedFeatureLayer."""

        derivedLayer = self.derivedLayer
        if derivedLayer is None:
            return

        qgsInfo(f"Repersisting derived features for layer {self.name()} …")
        self.setReadOnly(False)

        try:
            with Edits.editAndCommit(self):
                self.dataProvider().truncate()
                
                derivedFeatures = list(derivedLayer.getFeatures())
                for derivedFeature in derivedFeatures:
                    feature = self.copyFeature(derivedFeature)
                    feature.upsert()
        finally:
            self.setReadOnly(True)
            self.featuresChanged.emit([])
            self.triggerRepaint()
            
            
    @pyqtSlot()
    def onWorkspaceConnectionChanged(self):      
        return super().onWorkspaceConnectionChanged()
    
    