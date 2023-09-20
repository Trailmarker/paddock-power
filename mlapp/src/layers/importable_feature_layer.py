# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsProject

from ..utils import PLUGIN_NAME, qgsInfo
from .features import Edits
from .fields import FeatureStatus
from .interfaces import IImportableFeatureLayer, IStatusFeature
from .persisted_feature_layer import PersistedFeatureLayer


class ImportableFeatureLayer(PersistedFeatureLayer, IImportableFeatureLayer):

    def __init__(self, workspaceFile, layerName, styleName=None):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""

        super().__init__(workspaceFile, layerName, styleName)

    def makeImportFeatureRequest(self):
        """Return a QgsFeatureRequest with this layer as destination."""
        return QgsFeatureRequest().setDestinationCrs(self.crs(), QgsProject.instance().transformContext())

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
        unfilteredImportFeatures = [feature for feature in importLayer.getFeatures()]
        importFeatures = [feature for feature in importLayer.getFeatures(importFilter)]

        filteredCount = len(unfilteredImportFeatures) - len(importFeatures)
        qgsInfo(f"Filtering {filteredCount} features based on rules (for example if outside Property neighbourhood).")
        qgsInfo(f"Importing {len(importFeatures)} features into layer {self.name()} via field map {fieldMap} …")

        for importQgsFeature in importFeatures:
            raiseErrorIfTaskHasBeenCancelled()
            targetFeature = self.mapFeature(importQgsFeature, fieldMap)
            features.append(targetFeature)

        # Import as a bulkAdd
        return edits.editBefore(Edits.bulkAdd(self, features))
