# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..features.edits import Edits
from ..features.paddock import Paddock
from .condition_table import ConditionTable
from .status_feature_layer import StatusFeatureLayer


class PaddockLayer(StatusFeatureLayer):

    STYLE = "paddock"

    def getFeatureType(self):
        return Paddock

    def __init__(self, project, gpkgFile, layerName, conditionTable: ConditionTable):
        """Create or open a Paddock layer."""

        super().__init__(project, gpkgFile, layerName, styleName=PaddockLayer.STYLE)

        self._paddockLandSystemsLayerId = None
        self._derivedMetricPaddockLayerId = None
        self.conditionTable = conditionTable

    @property
    def paddockLandSystemsLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLandSystemsLayerId) if self._paddockLandSystemsLayerId else None

    @paddockLandSystemsLayer.setter
    def paddockLandSystemsLayer(self, paddockLandSystemsLayer):
        self._paddockLandSystemsLayerId = paddockLandSystemsLayer.id()

    @property
    def derivedMetricPaddockLayer(self):
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId) if self._derivedMetricPaddockLayerId else None

    @derivedMetricPaddockLayer.setter
    def derivedMetricPaddockLayer(self, derivedMetricPaddockLayer):
        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id() if derivedMetricPaddockLayer else None

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.derivedMetricPaddockLayer, self.paddockLandSystemsLayer, self.conditionTable, feature)
