# -*- coding: utf-8 -*-
from .persisted_feature import PersistedFeature
from ..fields.schemas import PaddockLandTypeSchema
from ..layers.condition_table import ConditionTable


@PaddockLandTypeSchema.addSchema()
class PaddockLandType(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Paddock Condition."""
        super().__init__(featureLayer, existingFeature)

    @property
    def NAME(self):
        return f"{self.LAND_TYPE_NAME}"

    @property
    def TITLE(self):
        return f"{self.LAND_TYPE_NAME} ({self.AREA:.2f} km², {self.ESTIMATED_CAPACITY:.1f} AE)"

    @property
    def conditionTable(self):
        return self.workspaceLayer(ConditionTable)

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False

    def upsertCondition(self, conditionType):
        """Update the Condition table."""
        self.conditionTable.upsert(self.paddock, self.landType, conditionType)
        self.conditionType = conditionType
