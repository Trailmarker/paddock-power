# -*- coding: utf-8 -*-
from .features import LandType
from .imported_feature_layer import ImportedFeatureLayer


class LandTypeLayer(ImportedFeatureLayer):

    NAME = "Land Types"
    STYLE = "land_type"

    @classmethod
    def getFeatureType(cls):
        return LandType

    def __init__(self, workspaceFile):
        super().__init__(workspaceFile,
                         layerName=LandTypeLayer.NAME,
                         styleName=LandTypeLayer.STYLE)

        self.setReadOnly(True)
