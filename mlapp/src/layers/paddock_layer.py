# -*- coding: utf-8 -*-
from .features import Paddock
from .imported_feature_layer import ImportedFeatureLayer


class PaddockLayer(ImportedFeatureLayer):

    LAYER_NAME = "Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return Paddock

    def __init__(self,
                 workspaceFile: str,
                 conditionTable):
        """Create or open a Paddock layer."""

        super().__init__(workspaceFile,
                         layerName=PaddockLayer.defaultName(),
                         styleName=PaddockLayer.defaultStyle())

    def getFeaturesByStatus(self, *statuses, request=None):
        """Get the features in this layer filtered by one or more FeatureStatus values."""
        if not statuses:
            return self.getFeatures(request)
        return [f for f in self.getFeatures(request) if f.STATUS.match(*statuses)]
