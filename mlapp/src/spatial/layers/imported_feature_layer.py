# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from ...utils import PLUGIN_NAME, qgsDebug, qgsInfo
from ..features.edits import Edits
from ..features.status_feature import StatusFeature
from ..fields.feature_status import FeatureStatus
from .persisted_feature_layer import PersistedFeatureLayer


class ImportedFeatureLayer(PersistedFeatureLayer):

    def __init__(self, featureType, workspaceFile, layerName, styleName=None):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""

        super().__init__(featureType, workspaceFile, layerName, styleName)

    def mapFeature(self, importFeature, fieldMap):
        f"""Map a QgsFeature to a {PLUGIN_NAME} Feature."""

        targetFeature = self.makeFeature()
        mappedFeature = fieldMap.mapFeature(importFeature, targetFeature)
        feature = self.wrapFeature(mappedFeature)
        feature.clearId()

        # Default imported data to 'Built' status - TODO might need other things here?
        if isinstance(feature, StatusFeature):
            feature.status = FeatureStatus.Built

        return feature

    @pyqtSlot()
    def importFeatures(self, importLayer, fieldMap):
        """Import all Features from the specified layer, applying the given field map."""
        qgsInfo(f"Importing features for layer {self.name()} …")

        wasReadOnly = self.readOnly()
        self.setReadOnly(False)
        try:
            with Edits.editAndCommit(self):
                self.dataProvider().truncate()
                features = [self.mapFeature(qf, fieldMap) for qf in list(importLayer.getFeatures())]
                qgsDebug(f"Features to import: {[format(f) for f in features]}")
                for feature in features:
                    feature.upsert()
                return features
        finally:
            self.setReadOnly(wasReadOnly)
            self.featuresChanged.emit([])
            self.triggerRepaint()
