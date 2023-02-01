# -*- coding: utf-8 -*-
from ..fields import PaddockLandTypeSchema
from .land_type_condition import LandTypeCondition
from .edits import Edits
from .persisted_feature import PersistedFeature


@PaddockLandTypeSchema.addSchema()
class PaddockLandType(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Paddock Condition."""
        super().__init__(featureLayer, existingFeature)
        self._conditionType = None

    @property
    def NAME(self):
        return f"{self.LAND_TYPE_NAME}"

    @property
    def TITLE(self):
        return f"{self.LAND_TYPE_NAME} ({self.AREA:.2f} km², {self.ESTIMATED_CAPACITY:.1f} AE)"

    @property
    def conditionType(self):
        return self._conditionType if self._conditionType else self.CONDITION_TYPE

    @conditionType.setter
    def conditionType(self, ct):
        self._conditionType = ct

    @classmethod
    def focusOnSelect(cls):
        return False

    def delete(self):
        return Edits.delete()

    def recalculate(self):
        pass

    def upsert(self):
        record = LandTypeCondition(self.PADDOCK, self.LAND_TYPE, self.conditionType)
        return Edits.upsert(record)
