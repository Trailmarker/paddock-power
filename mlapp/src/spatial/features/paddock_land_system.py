# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from .feature import Feature
from ..schemas.schemas import PaddockLandSystemSchema


@PaddockLandSystemSchema.addSchema()
class PaddockLandSystem(Feature):
    featureUpdated = pyqtSignal()

    def __init__(self, featureLayer, conditionTable, existingFeature):
        """Create a new Paddock Condition."""
        super().__init__(featureLayer, existingFeature)

        self.conditionTable = conditionTable

    @property
    def name(self):
        return f"{self.landSystemName}"

    def upsertCondition(self, conditionType):
        """Update the Condition table."""
        self.conditionTable.upsert(self.paddock, self.landSystem, conditionType)
        self.conditionType = conditionType
        self.featureUpdated.emit()
