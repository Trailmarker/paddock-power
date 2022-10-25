# -*- coding: utf-8 -*-
from .edits import Edits
from .feature import Feature
from .schemas import WaterpointBufferSchema


@WaterpointBufferSchema.addSchema()
class WaterpointBuffer(Feature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Boundary."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    def createFeature(self, waterpoint, geometry, waterpointBufferType, bufferDistance):
        self.waterpoint = waterpoint.id
        self.geometry = geometry
        self.waterpointBufferType = waterpointBufferType
        self.bufferDistance = bufferDistance
        return Edits.upsert(self)

    def deleteFeature(self):
        self.waterpoint = None
        return Edits.delete(self)
