# -*- coding: utf-8 -*-
from .features import LandType
from .imported_feature_layer import ImportedFeatureLayer


class LandTypeLayer(ImportedFeatureLayer):

    LAYER_NAME = "Land Types"
    STYLE = "land_type"

    @classmethod
    def getFeatureType(cls):
        return LandType

    def __init__(self, workspaceFile):
        super().__init__(workspaceFile,
                         layerName=LandTypeLayer.defaultName(),
                         styleName=LandTypeLayer.defaultStyle())

        self.setReadOnly(True)
