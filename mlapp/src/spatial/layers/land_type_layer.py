# -*- coding: utf-8 -*-
from ..features.land_type import LandType
from .imported_feature_layer import ImportedFeatureLayer


class LandTypeLayer(ImportedFeatureLayer):

    STYLE = "land_type"

    def getFeatureType(self):
        return LandType

    def __init__(self, project, gpkgFile, layerName):
        super().__init__(project,
                         gpkgFile,
                         layerName,
                         styleName=LandTypeLayer.STYLE)

        self.setReadOnly(True)
