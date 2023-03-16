# -*- coding: utf-8 -*-
from .features import BasePaddock
from .importable_feature_layer import ImportableFeatureLayer
from .status_feature_layer_mixin import StatusFeatureLayerMixin


class BasePaddockLayer(ImportableFeatureLayer, StatusFeatureLayerMixin):

    LAYER_NAME = "Base Paddocks"
    STYLE = "base_paddock"

    @classmethod
    def getFeatureType(cls):
        return BasePaddock

    def __init__(self,
                 workspaceFile):
        """Create or open a Paddock layer."""

        super().__init__(workspaceFile,
                         layerName=BasePaddockLayer.defaultName(),
                         styleName=BasePaddockLayer.defaultStyle())
