# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...utils import qgsDebug
from ..features.paddock import MetricPaddock
from .condition_table import ConditionTable
from .status_feature_layer import StatusFeatureLayer


class PaddockLayer(StatusFeatureLayer):

    STYLE = "paddock"

    def getFeatureType(self):
        return MetricPaddock

    def __init__(self, project, gpkgFile, layerName, conditionTable: ConditionTable):
        """Create or open a Paddock layer."""

        super().__init__(project, gpkgFile, layerName, styleName=PaddockLayer.STYLE)

        self._paddockLandTypesLayerId = None
        self._derivedMetricPaddockLayerId = None
        self.conditionTable = conditionTable

    @property
    def paddockLandTypesLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLandTypesLayerId) if self._paddockLandTypesLayerId else None

    @paddockLandTypesLayer.setter
    def paddockLandTypesLayer(self, paddockLandTypesLayer):
        self._paddockLandTypesLayerId = paddockLandTypesLayer.id()

    @property
    def derivedMetricPaddockLayer(self):
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId) if self._derivedMetricPaddockLayerId else None

    @derivedMetricPaddockLayer.setter
    def derivedMetricPaddockLayer(self, derivedMetricPaddockLayer):
        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id() if derivedMetricPaddockLayer else None

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.derivedMetricPaddockLayer, self.paddockLandTypesLayer, self.conditionTable, feature)
