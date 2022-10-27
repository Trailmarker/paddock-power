# -*- coding: utf-8 -*-
from ..schemas.schemas import WaterpointBufferSchema
from .edits import Edits
from .feature import Feature
from .feature_action import FeatureAction


@WaterpointBufferSchema.addSchema()
class WaterpointBuffer(Feature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Boundary."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

    @FeatureAction.plan.handler()
    def planFeature(self, waterpoint, geometry, waterpointBufferType, bufferDistance):
        self.waterpoint = waterpoint.id
        self.geometry = geometry
        self.waterpointBufferType = waterpointBufferType
        self.bufferDistance = bufferDistance
        return Edits.upsert(self)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        self.waterpoint = None
        return Edits.delete(self)

    @FeatureAction.build.handler()
    def buildFeature(self):
        return Edits.upsert(self)

    @FeatureAction.undoBuild.handler()
    def undoBuildFeature(self):
        return Edits.upsert(self)
