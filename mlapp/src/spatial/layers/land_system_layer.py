# -*- coding: utf-8 -*-
from ..features.land_system import LandSystem
from .persisted_feature_layer import PersistedFeatureLayer


class LandSystemLayer(PersistedFeatureLayer):

    STYLE = "land_system"

    def getFeatureType(self):
        return LandSystem

    def __init__(self, gpkgFile, layerName):
        super().__init__(gpkgFile,
                         layerName,
                         styleName=LandSystemLayer.STYLE)
