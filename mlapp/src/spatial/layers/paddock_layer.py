# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsProject

from ..features.edits import Edits
from ..features.paddock import Paddock
from ..schemas.schemas import RECALCULATE_COMPLETE, RECALCULATE_CURRENT
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
                 conditionTable: ConditionTable):
        """Create or open a Paddock layer."""

        super().__init__(gpkgFile, layerName, styleName=PaddockLayer.STYLE)

        self._landSystemLayerId = landSystemLayer.id()
        self._waterpointBufferLayerId = None
        self.conditionTable = conditionTable

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId) if self._waterpointBufferLayerId else None

    @waterpointBufferLayer.setter
    def waterpointBufferLayer(self, waterpointBufferLayer):
        self._waterpointBufferLayerId = waterpointBufferLayer.id()

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.landSystemLayer, self.waterpointBufferLayer, self.conditionTable, feature)

    def getRecalculateBatchNumber(self):
        """The lowest Build Order of any Fence in Draft status."""

        fieldIndex = self.fields().indexFromName(RECALCULATE_CURRENT)
        try:
            return self.maximumValue(fieldIndex) + 1
        finally:
            return 1

    def getRecalculateBatchEdits(self, batchNumber):
        """Get the edits for the current recalculate batch."""

        recalculateBatchRequest = QgsFeatureRequest().setFilterExpression(f'("{RECALCULATE_CURRENT}"={batchNumber}) and ("{RECALCULATE_COMPLETE}" is null)')
        features = list(self.getFeatures(request=recalculateBatchRequest))
        return Edits.upsert(*features)