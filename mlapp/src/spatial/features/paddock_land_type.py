# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from .persisted_feature import PersistedFeature
from ..fields.schemas import PaddockLandTypeSchema


@PaddockLandTypeSchema.addSchema()
class PaddockLandType(PersistedFeature):
    featureUpdated = pyqtSignal()

    def __init__(self, featureLayer, conditionTable, existingFeature):
        """Create a new Paddock Condition."""
        super().__init__(featureLayer, existingFeature)

        self.conditionTable = conditionTable

    @property
    def name(self):
        return f"{self.landTypeName}"

    @property
    def title(self):
        return f"{self.landTypeName} ({self.featureArea:.2f} km², {self.estimatedCapacity:.1f} AE)"

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False

    def upsertCondition(self, conditionType):
        """Update the Condition table."""
        self.conditionTable.upsert(self.paddock, self.landType, conditionType)
        self.conditionType = conditionType
        self.featureUpdated.emit()
