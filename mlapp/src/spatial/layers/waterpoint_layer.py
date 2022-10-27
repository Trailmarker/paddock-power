# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..features.waterpoint import Waterpoint
from .elevation_layer import ElevationLayer
from .status_feature_layer import StatusFeatureLayer


class WaterpointLayer(StatusFeatureLayer):

    STYLE = "waterpoint"

    @classmethod
    def getFeatureType(cls):
        return Waterpoint

    def __init__(self, gpkgFile, layerName,
                 elevationLayer: ElevationLayer):
        """Create or open a Waterpoint layer."""

        super().__init__(gpkgFile, layerName, styleName=WaterpointLayer.STYLE)

        self._waterpointBufferLayerId = None
        self._elevationLayerId = elevationLayer.id() if elevationLayer else None

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId) if self._waterpointBufferLayerId else None

    @waterpointBufferLayer.setter
    def waterpointBufferLayer(self, waterpointBufferLayer):
        self._waterpointBufferLayerId = waterpointBufferLayer.id()

    @property
    def elevationLayer(self):
        return QgsProject.instance().mapLayer(self._elevationLayerId) if self._elevationLayerId else None

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.waterpointBufferLayer, self.elevationLayer, feature)
