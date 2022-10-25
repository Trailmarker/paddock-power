# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..features.waterpoint import Waterpoint
from .elevation_layer import ElevationLayer
from .status_feature_layer import StatusFeatureLayer
from .waterpoint_buffer_layer import WaterpointBufferLayer


class WaterpointLayer(StatusFeatureLayer):

    STYLE = "waterpoint"

    @classmethod
    def getFeatureType(cls):
        return Waterpoint

    def __init__(self, gpkgFile, layerName,
                 waterpointBufferLayer: WaterpointBufferLayer,
                 elevationLayer: ElevationLayer):
        """Create or open a Waterpoint layer."""

        super().__init__(gpkgFile, layerName, styleName=WaterpointLayer.STYLE)

        self._waterpointBufferLayerId = waterpointBufferLayer.id()
        self._elevationLayerId = elevationLayer.id()

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId)

    @property
    def elevationLayer(self):
        return QgsProject.instance().mapLayer(self._elevationLayerId)


    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.waterpointBufferLayer, self.elevationLayer, feature)
