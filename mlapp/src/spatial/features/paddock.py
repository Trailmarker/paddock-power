# -*- coding: utf-8 -*-
from mlapp.src.spatial.layers.watered_area_layer import WateredAreaLayer
from qgis.core import QgsFeatureRequest, QgsProject

from ...models.glitch import Glitch
from ..layers.condition_record_layer import ConditionRecordLayer
from ..layers.land_system_layer import LandSystemLayer
from ..layers.watered_area_layer import WateredAreaLayer
from .area_feature import AreaFeature
from .condition_record import ConditionRecord
from .edits import Edits
from .feature_action import FeatureAction
from .schemas import PADDOCK, PaddockSchema


@PaddockSchema.addSchema()
class Paddock(AreaFeature):

    def __init__(self, featureLayer, landSystemLayer: LandSystemLayer, wataredAreaLayer: WateredAreaLayer, 
                 conditionRecordLayer: ConditionRecordLayer,  existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature=existingFeature)

        self._landSystemLayerId = landSystemLayer.id()
        self._wateredAreaLayerId = wataredAreaLayer.id()
        self._conditionRecordLayerId = conditionRecordLayer.id()

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def wataredAreaLayer(self):
        return QgsProject.instance().mapLayer(self._wateredAreaLayerId)

    @property
    def conditionRecordLayer(self):
        return QgsProject.instance().mapLayer(self._conditionRecordLayerId)

    @Glitch.glitchy()
    def getConditionRecordsForPaddock(self):
        paddockRequest = QgsFeatureRequest().setFilterExpression(
            f'"{PADDOCK}" = {self.id}')
        
        return list(self.conditionRecordLayer.getFeatures(paddockRequest))

    @Glitch.glitchy()
    def analyseConditionRecords(self):
        """Get the land systems that intersect this paddock."""

        landSystems = (self.landSystemLayer.getFeatures(self.geometry.boundingBox()))
        near, far = self.waterpointBufferLayer.getNearAndFarBuffers()

        overLandSystems = [record 
                           for landSystem in landSystems if landSystem.geometry.intersects(self.geometry)
                           for record in ConditionRecord.fromPaddockAndLandSystem(self.conditionRecordLayer, self, landSystem)]

        overNearBuffer = [record for unwatered in overLandSystems 
                          for record in unwatered.overWaterpointBuffer(near)]

        overFarBuffer = [record for unwatered in overLandSystems 
                         for record in unwatered.overWaterpointBuffer(far)]

        return (overNearBuffer + overFarBuffer), self.getConditionRecordsForPaddock()
   
    def analyseFeature(self):
        """Analyse the feature."""
        super().recalculate() # Re-check the area and perimeter
        
        edits = Edits()

        conditionRecords, currentConditionRecords = self.analyseConditionRecords()

        for record in conditionRecords:
            record.recalculate()

        self.estimatedCapacity = sum([record.estimatedCapacity for record in conditionRecords])
        self.potentialCapacity = sum([record.potentialCapacity for record in conditionRecords])
        self.capacityPerArea = self.estimatedCapacity / self.featureArea

        edits.editBefore(Edits.delete(*currentConditionRecords))
        edits.editBefore(Edits.upsert(*conditionRecords))
        return edits

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
