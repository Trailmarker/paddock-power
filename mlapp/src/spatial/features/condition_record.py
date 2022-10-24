# -*- coding: utf-8 -*-
from qgis.core import QgsProject

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

        self._paddockLayerId = paddockLayer.id()
        self._landSystemLayerId = landSystemLayer.id()
        self._waterpointBufferLayerId = waterpointBufferLayer.id()

    @property
    def paddockLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLayerId)

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId)
