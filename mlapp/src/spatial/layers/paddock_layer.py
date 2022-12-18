# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsProject

from ...utils import qgsDebug
from ..features.edits import Edits
from ..features.paddock import Paddock
from ..schemas.schemas import RECALCULATE_COMPLETE, RECALCULATE_CURRENT
from .condition_table import ConditionTable
from .land_system_layer import LandSystemLayer
from .status_feature_layer import StatusFeatureLayer


class PaddockLayer(StatusFeatureLayer):

    STYLE = "paddock"

    def getFeatureType(self):
        return Paddock

    def __init__(self, project, gpkgFile, layerName, landSystemLayer: LandSystemLayer,
                 conditionTable: ConditionTable):
        """Create or open a Paddock layer."""

        super().__init__(project, gpkgFile, layerName, styleName=PaddockLayer.STYLE)

        self._landSystemLayerId = landSystemLayer.id()
        self._wateredAreaLayerId = None
        self.conditionTable = conditionTable

        # Recalculate when our dependencies change
        # self.landSystemLayer.featuresPersisted.connect(self.recalculateAll)
        # self.conditionTable.conditionRecordsUpdated.connect(self.recalculateId)

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def wateredAreaLayer(self):
        return QgsProject.instance().mapLayer(self._wateredAreaLayerId) if self._wateredAreaLayerId else None

    @wateredAreaLayer.setter
    def wateredAreaLayer(self, wateredAreaLayer):
        self._wateredAreaLayerId = wateredAreaLayer.id()
        # Recalculate when our dependencies change
        # wateredAreaLayer.featuresPersisted.connect(self.recalculateAll)

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.landSystemLayer, self.wateredAreaLayer, self.conditionTable, feature)

    @Edits.persistFeatures
    def recalculateId(self, id):
        """Recalculate all Paddock metrics for a specific Paddock."""
        qgsDebug(f"PaddockLayer.recalculateId({id})")
        # return Edits()
        try:
            paddock = self.getFeature(id)
            if paddock:
                paddock.recalculate()
                return Edits.upsert(paddock)
            else:
                qgsDebug("Couldn't get matching paddock")
                return Edits()
        except BaseException:
            return Edits()

    @Edits.persistFeatures
    def recalculateAll(self):
        """Recalculate all Paddock statistics."""
        paddocks = [p for p in self.getFeatures()]
        for paddock in paddocks:
            paddock.recalculate()
        return Edits.upsert(*paddocks)

    def getRecalculateBatchNumber(self):
        """The lowest Build Order of any Fence in Draft status."""

        fieldIndex = self.fields().indexFromName(RECALCULATE_CURRENT)
        try:
            return self.maximumValue(fieldIndex) + 1
        finally:
            return 1

    def getRecalculateBatchEdits(self, batchNumber):
        """Get the edits for the current recalculate batch."""

        recalculateBatchRequest = QgsFeatureRequest().setFilterExpression(
            f'("{RECALCULATE_CURRENT}"={batchNumber}) and ("{RECALCULATE_COMPLETE}" is null)')
        features = list(self.getFeatures(request=recalculateBatchRequest))
        return Edits.upsert(*features)
