# -*- coding: utf-8 -*-
from abc import abstractmethod
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsProject

from ...utils import PLUGIN_NAME, qgsInfo
from .derived_feature_layer import DerivedFeatureLayer
from .persisted_feature_layer import PersistedFeatureLayer
from ..features.edits import Edits


class PersistedDerivedFeatureLayer(PersistedFeatureLayer):

    @abstractmethod
    def getFeatureType(self):
        """Return the type of feature that this layer contains, which depnds on the underlying derived layer. Override in subclasses."""
        pass

    def __init__(self, gpkgFile, layerName, derivedLayer, styleName=None):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""

        assert(isinstance(derivedLayer, DerivedFeatureLayer))

        # Set the derived (virtual) layer that will be used to update this one
        self._derivedLayerId = derivedLayer.id()

        # Ensures that the layer is created in the GeoPackage
        # Adjusts the schema to match the feature type
        # Applies the editor widgets (TODO need to make read only for a derived layer?)
        # Optionally applies a style
        super().__init__(gpkgFile, layerName, styleName=styleName)

        # Connect persistence on upstream PersistedFeatureLayers to the deriveFeatures slot
        for featureLayer in self.derivedLayer.persistedFeatureLayers:
            featureLayer.featuresPersisted.connect(self.repersistDerivedFeatures)

        self.repersistDerivedFeatures()

        self.setReadOnly(True)  # TODO?

    @property
    def derivedLayer(self):
        """Return the DerivedFeatureLayer that this layer persists features from."""
        return QgsProject.instance().mapLayer(self._derivedLayerId)

    @pyqtSlot()
    def repersistDerivedFeatures(self):
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
            self.featuresPersisted.emit()
            self.triggerRepaint()
