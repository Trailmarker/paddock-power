# -*- coding: utf-8 -*-
from ..features.land_type import LandSystem
from .persisted_feature_layer import PersistedFeatureLayer


class LandSystemLayer(PersistedFeatureLayer):

    STYLE = "land_type"

    def getFeatureType(self):
        return LandSystem

    def __init__(self, project, gpkgFile, layerName):
        super().__init__(project,
                         gpkgFile,
                         layerName,
                         styleName=LandSystemLayer.STYLE)

        self.setReadOnly(True)
