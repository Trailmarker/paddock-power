# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from .persisted_feature import PersistedFeature
from ..schemas.schemas import PaddockLandSystemSchema


@PaddockLandSystemSchema.addSchema()
class PaddockLandSystem(PersistedFeature):
    featureUpdated = pyqtSignal()

    def __init__(self, featureLayer, conditionTable, existingFeature):
        """Create a new Paddock Condition."""
        super().__init__(featureLayer, existingFeature)

        self.conditionTable = conditionTable

    @property
    def name(self):
        return f"{self.landSystemName}"

    @property
    def title(self):
        return f"{self.landSystemName} ({self.featureArea:.2f} km², {self.estimatedCapacity:.1f} AE)"

    @property
    def focusOnSelect(self):
        """Return True if the app should focus on this Feature when selected."""
        return False

    def upsertCondition(self, conditionType):
        """Update the Condition table."""
        self.conditionTable.upsert(self.paddock, self.landSystem, conditionType)
        self.conditionType = conditionType
        self.featureUpdated.emit()
