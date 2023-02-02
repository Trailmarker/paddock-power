# -*- coding: utf-8 -*-
from .features import Paddock
from .imported_feature_layer import ImportedFeatureLayer
from .status_feature_layer_mixin import StatusFeatureLayerMixin


class PaddockLayer(ImportedFeatureLayer, StatusFeatureLayerMixin):

    LAYER_NAME = "Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return Paddock

    def __init__(self,
                 workspaceFile):
        """Create or open a Paddock layer."""

        super().__init__(workspaceFile,
                         layerName=PaddockLayer.defaultName(),
                         styleName=PaddockLayer.defaultStyle())
