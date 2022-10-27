# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..features.paddock import Paddock
from .condition_table import ConditionTable
from .waterpoint_buffer_layer import WaterpointBufferLayer
from .land_system_layer import LandSystemLayer
from .status_feature_layer import StatusFeatureLayer


class PaddockLayer(StatusFeatureLayer):

    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return Paddock

    def __init__(self, gpkgFile, layerName, landSystemLayer: LandSystemLayer,
                 waterpointBufferLayer: WaterpointBufferLayer, conditionTable: ConditionTable):
        """Create or open a Paddock layer."""

        super().__init__(gpkgFile, layerName, styleName=PaddockLayer.STYLE)

        self._landSystemLayerId = landSystemLayer.id()
        self._waterpointBufferLayerId = waterpointBufferLayer.id()
        self.conditionTable = conditionTable

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId)

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.landSystemLayer, self.waterpointBufferLayer, self.conditionTable, feature)
