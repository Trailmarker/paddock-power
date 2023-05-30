# -*- coding: utf-8 -*-
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

    def importFeatures(self, importLayer, fieldMap, importFilter=None, raiseErrorIfTaskHasBeenCancelled=lambda: None):
        """Import all Features from the specified layer, applying the given field map."""
        edits = Edits.truncate(self)

        features = []
        importQgsFeatures = [importFeature for importFeature in importLayer.getFeatures(importFilter)]

        qgsInfo(f"Importing {len(importQgsFeatures)} features into layer {self.name()} via field map {fieldMap} …")

        for importQgsFeature in importQgsFeatures:
            raiseErrorIfTaskHasBeenCancelled()
            targetFeature = self.mapFeature(importQgsFeature, fieldMap)
            features.append(targetFeature)

        # Import as a bulkAdd
        return edits.editBefore(Edits.bulkAdd(self, features))
