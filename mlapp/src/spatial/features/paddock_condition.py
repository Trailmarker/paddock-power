# -*- coding: utf-8 -*-
from .feature import Feature
from ..schemas.schemas import PaddockConditionSchema


@PaddockConditionSchema.addSchema()
class PaddockCondition(Feature):

    def __init__(self, featureLayer, conditionTable, existingFeature):
        """Create a new Paddock Condition."""
        super().__init__(featureLayer, existingFeature)

        self.conditionTable = conditionTable

    @property
    def name(self):
        return f"{self.landSystemName} (Watered: {self.wateredType.value})"

    @property
    def focusOnSelect(self):
        """Return True if the app should focus on this Feature when selected."""
        return False

