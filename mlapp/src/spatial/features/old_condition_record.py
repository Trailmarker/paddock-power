# -*- coding: utf-8 -*-
from ...models.glitch import Glitch
from ..calculator import Calculator
from .edits import Edits
from .persisted_feature import PersistedFeature
from ..schemas.schemas import OldConditionRecordSchema


@OldConditionRecordSchema.addSchema()
class OldConditionRecord(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    def recalculate(self):
        area = round(Calculator.calculateArea(self.geometry) / 1000000, 2)
        perimeter = round(Calculator.calculatePerimeter(self.geometry) / 1000, 2)
        self.featureArea = area
        self.featurePerimeter = perimeter
        self.estimatedCapacity = round(self.featureArea * self.capacityPerArea, 2) # TODO Discount rate
        self.potentialCapacity = round(self.featureArea * self.capacityPerArea, 2)

        return super().recalculate()

    def index(self):
        return (self.paddock, self.landSysten, self.waterpointBufferType)

    @classmethod
    @Glitch.glitchy()
    def fromPaddockAndLandSystem(cls, conditionRecordLayer, paddock, landSystem, intersection=None):
        if intersection is None:
            intersection = paddock.geometry.intersection(landSystem.geometry)

        if intersection.isEmpty():
            return []
        if intersection.isMultipart():
            return [record for part in intersection.asGeometryCollection()
                    for record in OldConditionRecord.fromPaddockAndLandSystem(conditionRecordLayer, paddock, landSystem, part)]

        record = conditionRecordLayer.makeFeature()
        record.geometry = intersection
        record.paddock = paddock.id
        record.paddockName = paddock.name
        record.status = paddock.status
        record.landSystem = landSystem.id
        record.landSystemName = landSystem.name
        record.capacityPerArea = landSystem.capacityPerArea
        return [record]

    @Glitch.glitchy()
    def overWaterpointBuffer(self, buffer, intersection=None):
        """Return a list of partial Condition records generated over the given 'Near' or 'Far' waterpoint buffer."""
        if intersection is None:
            intersection = self.geometry.intersection(buffer.geometry)

        if intersection.isEmpty():
            return []
        if intersection.isMultipart():
            return [record for part in intersection.asGeometryCollection()
                    for record in self.overWaterpointBuffer(buffer, part)]

        record = self.featureLayer.copyFeature(self)
        record.geometry = intersection
        record.waterpointBufferType = buffer.waterpointBufferType
        return [record]

    def deleteFeature(self):
        self.paddock = None
        self.landSystem = None
        self.waterpoint = None
        return Edits.delete(self)
