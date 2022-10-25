# -*- coding: utf-8 -*-
from ..features.land_system import LandSystem
from .feature_layer import FeatureLayer


class LandSystemLayer(FeatureLayer):

    # STYLE = "land_system"

    @classmethod
    def getFeatureType(cls):
        return LandSystem

    def __init__(self, gpkgFile, layerName):
        super().__init__(gpkgFile,
                         layerName,
                         styleName=None)
