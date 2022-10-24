# -*- coding: utf-8 -*-
from ..features.paddock import Paddock

from .feature_layer import FeatureLayer
# from .renderers import fillStatusCategoryRenderer


class PaddockLayer(FeatureLayer):

    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return Paddock

    def __init__(self, gpkgFile, layerName):
        """Create or open a Paddock layer."""

        super().__init__(gpkgFile, layerName, styleName=PaddockLayer.STYLE)

        # self.setRenderer(fillStatusCategoryRenderer())
