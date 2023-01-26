# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME, qgsDebug
from .persisted_feature_layer import PersistedFeatureLayer


class ImportedFeatureLayer(PersistedFeatureLayer):

    def __init__(self, *args, **kwargs):
        f"""Create a new {PLUGIN_NAME} derived persisted feature layer."""

        super().__init__(*args, **kwargs)

    def importFeature(self, fieldMap, qgsFeature):
        f"""Map a QgsFeature to a {PLUGIN_NAME} Feature."""
        # feature = self.wrapFeature(qgsFeature)
        # feature.mapToField(fieldMap)
        # return feature
        qgsDebug("Importing feature")
        pass
