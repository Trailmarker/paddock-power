# -*- coding: utf-8 -*-
from ..features.boundary import Boundary
from .feature_layer import FeatureLayer


class BoundaryLayer(FeatureLayer):

    STYLE = "boundary"

    @classmethod
    def getFeatureType(cls):
        return Boundary

    def __init__(self, gpkgFile, layerName):
        super().__init__(gpkgFile, layerName, styleName=BoundaryLayer.STYLE)
