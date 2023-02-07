# -*- coding: utf-8 -*-
from .features import BasePaddock
from .imported_feature_layer import ImportedFeatureLayer
from .status_feature_layer_mixin import StatusFeatureLayerMixin


class BasePaddockLayer(ImportedFeatureLayer, StatusFeatureLayerMixin):

    LAYER_NAME = "Base Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return BasePaddock

    def __init__(self,
                 workspaceFile):
        """Create or open a Paddock layer."""

        super().__init__(workspaceFile,
                         layerName=BasePaddockLayer.defaultName(),
                         styleName=BasePaddockLayer.defaultStyle())
