# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from ..utils import PLUGIN_NAME, qgsInfo
from .features import Edits
from .fields import FeatureStatus
from .interfaces import IImportableFeatureLayer, IStatusFeature
from .persisted_feature_layer import PersistedFeatureLayer


class ImportableFeatureLayer(PersistedFeatureLayer, IImportableFeatureLayer):

    def __init__(self, workspaceFile, layerName, styleName=None):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""

        super().__init__(workspaceFile, layerName, styleName)

    def mapFeature(self, importFeature, fieldMap):
        f"""Map a QgsFeature to a {PLUGIN_NAME} Feature."""

        targetFeature = self.makeFeature()
        mappedFeature = fieldMap.mapFeature(importFeature, targetFeature)
        feature = self.wrapFeature(mappedFeature)

        # Default imported data to 'Built' status - TODO might need other things here?
        if isinstance(feature, IStatusFeature):
            feature.STATUS = FeatureStatus.Built

        return feature

    @pyqtSlot()
    def importFeatures(self, importLayer, fieldMap):
        """Import all Features from the specified layer, applying the given field map."""
        qgsInfo(f"Importing features for layer {self.name()} …")

        edits = Edits.truncate(self)
        features = [self.mapFeature(qf, fieldMap) for qf in list(importLayer.getFeatures())]

        # Import as a bulkAdd
        return edits.editBefore(Edits.bulkAdd(self, features))