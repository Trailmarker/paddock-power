# -*- coding: utf-8 -*-
from ..features.land_type import LandType
from .imported_feature_layer import ImportedFeatureLayer


class LandTypeLayer(ImportedFeatureLayer):

    NAME = "Land Types"
    STYLE = "land_type"

    def __init__(self, workspaceFile):
        super().__init__(LandType,
                         workspaceFile,
                         layerName=LandTypeLayer.NAME,
                         styleName=LandTypeLayer.STYLE)

        self.setReadOnly(True)
