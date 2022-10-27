# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from .feature import Feature
from ..schemas.schemas import ConditionSchema


@ConditionSchema.addSchema()
class Condition(Feature):
    featureUpdated = pyqtSignal()

    def __init__(self, featureLayer, conditionTable, existingFeature):
        """Create a new Boundary."""
        super().__init__(featureLayer, existingFeature)

        self.conditionTable = conditionTable

    @property
    def name(self):
        return f"{'Unknown Land System'} ({self.wateredType.value})"

    def upsertCondition(self, conditionType):
        """Update the Condition table."""
        self.conditionTable.upsert(self.paddock, self.landSystem, self.wateredType, conditionType)
        self.featureUpdated.emit()
