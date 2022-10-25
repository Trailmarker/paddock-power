# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..layers.condition_record_layer import ConditionRecordLayer
from ..layers.land_system_layer import LandSystemLayer
from ..layers.waterpoint_buffer_layer import WaterpointBufferLayer
from .area_feature import AreaFeature
from .edits import Edits
from .feature_action import FeatureAction
from .schemas import PaddockSchema


@PaddockSchema.addSchema()
class Paddock(AreaFeature):

    def __init__(self, featureLayer, landSystemLayer: LandSystemLayer, waterpointBufferLayer: WaterpointBufferLayer, 
                 conditionRecordLayer: ConditionRecordLayer,  existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature=existingFeature)

        self._landSystemLayerId = landSystemLayer.id()
        self._waterpointBufferLayerId = waterpointBufferLayer.id()
        self._conditionRecordLayerId = conditionRecordLayer.id()

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId)

    @property
    def conditionRecordLayer(self):
        return QgsProject.instance().mapLayer(self._conditionRecordLayerId)

    @FeatureAction.draft.handler()
    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        self.name = name
        self.geometry = geometry
        return Edits.upsert(self)

    @FeatureAction.plan.handler()
    def planFeature(self, fence):
        self.buildFence = fence.buildOrder
        return Edits.upsert(self)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        self.buildFence = None
        return Edits.delete(self)

    @FeatureAction.supersede.handler()
    def supersedeFeature(self, fence):
        self.buildFence = fence.buildOrder
        return Edits.upsert(self)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        self.buildFence = None
        return Edits.upsert(self)
