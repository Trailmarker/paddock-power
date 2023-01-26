# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsProject

from ...utils import PLUGIN_NAME, qgsInfo
from .derived_feature_layer import DerivedFeatureLayer
from .persisted_feature_layer import PersistedFeatureLayer
from ..features.edits import Edits


class PersistedDerivedFeatureLayer(PersistedFeatureLayer):

    def __init__(self, project, gpkgFile, layerName, derivedLayer, styleName=None):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""

        assert(isinstance(derivedLayer, DerivedFeatureLayer))

        # Set the derived (virtual) layer that will be used to update this one
        self._derivedLayerId = derivedLayer.id()

        # Ensures that the layer is created in the GeoPackage
        # Adjusts the schema to match the feature type
        # Applies the editor widgets (TODO need to make read only for a derived layer?)
        # Optionally applies a style
        super().__init__(project, gpkgFile, layerName, styleName=styleName)

        # Connect persistence on upstream PersistedFeatureLayers to the repersistDerivedFeatures slot
        for featureLayer in self.derivedLayer.persistedFeatureLayers:
            featureLayer.featuresPersisted.connect(lambda idList: self.repersistDerivedFeatures(featureLayer, idList))

        # Initial persistence
        self.repersistDerivedFeatures(None, [])

        self.setReadOnly(True)  # TODO?

    @property
    def derivedLayer(self):
        """Return the DerivedFeatureLayer that this layer persists features from."""
        return QgsProject.instance().mapLayer(self._derivedLayerId)

    @pyqtSlot()
    def repersistDerivedFeatures(self, layer, idList):
        """Derive all Features to be persisted from the source DerivedFeatureLayer."""
        qgsInfo(f"Repersisting derived features for layer {self.name()} …")
        self.setReadOnly(False)
        try:
            with Edits.editAndCommit(self):
                self.dataProvider().truncate()
                features = list(self.derivedLayer.getFeatures())
                self.addFeatures(features)
        finally:
            self.setReadOnly(True)
            self.featuresPersisted.emit([])
            self.triggerRepaint()
