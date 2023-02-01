# -*- coding: utf-8 -*-
from ..utils import PLUGIN_NAME
from .persisted_feature_layer import PersistedFeatureLayer


class StatusFeatureLayer(PersistedFeatureLayer):

    def __init__(self, workspaceFile, layerName, styleName=None):
        f"""Create a new {PLUGIN_NAME} status feature layer."""

        super().__init__(workspaceFile, layerName, styleName)

    def getFeaturesByStatus(self, *statuses, request=None):
        """Get the features in this layer filtered by one or more FeatureStatus values."""
        if not statuses:
            return self.getFeatures(request)
        return [f for f in self.getFeatures(request) if f.status.match(*statuses)]
