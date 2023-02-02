# -*- coding: utf-8 -*-
from ..fields import PaddockLandTypeSchema
from .derived_feature import DerivedFeature
from .land_type_condition import LandTypeCondition


@PaddockLandTypeSchema.addSchema()
class PaddockLandType(DerivedFeature):
    @classmethod
    def focusOnSelect(cls):
        return False

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Paddock Condition."""
        super().__init__(featureLayer, existingFeature)
        self._conditionType = None

    @property
    def landTypeCondition(self):
        """Get the Condition Record for this Paddock Land Type."""
        return LandTypeCondition(self.PADDOCK, self.LAND_TYPE, self.CONDITION_TYPE)

    @property
    def NAME(self):
        return f"{self.LAND_TYPE_NAME}"

    @property
    def TITLE(self):
        return f"{self.LAND_TYPE_NAME} ({self.AREA:.2f} km², {self.ESTIMATED_CAPACITY:.1f} AE)"
