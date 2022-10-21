# -*- coding: utf-8 -*-
from ..layers.land_system_layer import LandSystemLayer
from ..layers.paddock_layer import PaddockLayer
from ..layers.waterpoint_buffer_layer import WaterpointBufferLayer
from .capacity_feature import CapacityFeature
from .schemas import ConditionRecordSchema


@ConditionRecordSchema.addSchema()
class ConditionRecord(CapacityFeature):

    def __init__(self, featureLayer, paddockLayer: PaddockLayer, landSystemLayer: LandSystemLayer,
                 waterpointBufferLayer: WaterpointBufferLayer, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

        self.paddockLayer = paddockLayer
        self.landSystemLayer = landSystemLayer
        self.waterpointBufferLayer = waterpointBufferLayer

    
