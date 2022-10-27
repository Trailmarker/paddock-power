# -*- coding: utf-8 -*-
from qgis.core import QgsProject, QgsLayerTreeLayer

from ..layers.condition_table import ConditionTable
from ..layers.land_system_layer import LandSystemLayer
from ..layers.paddock_condition_layer import PaddockConditionLayer
from ..layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..schemas.schemas import PaddockSchema
from .area_feature import AreaFeature
from .edits import Edits
from .feature_action import FeatureAction


@PaddockSchema.addSchema()
class Paddock(AreaFeature):

    def __init__(self, featureLayer, landSystemLayer: LandSystemLayer, waterpointBufferLayer: WaterpointBufferLayer,
                 conditionTable: ConditionTable, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature=existingFeature)

        self._landSystemLayerId = landSystemLayer.id()
        self._waterpointBufferLayerId = waterpointBufferLayer.id()
        self.conditionTable = conditionTable

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId)

    @property
    def conditionRecordLayer(self):
        return QgsProject.instance().mapLayer(self._conditionRecordLayerId)

    def addConditionLayer(self):
        """Add a condition layer to the project."""
        item = QgsProject.instance().layerTreeRoot().findLayer(self.featureLayer)
        if not item:
            # If the Paddocks layer isn't in the map, don't initialise or add the condition layer.
            return
        self.conditionLayer = PaddockConditionLayer(
            f"{self.name} Paddock Condition",
            self,
            self.featureLayer,
            self.landSystemLayer,
            self.waterpointBufferLayer,
            self.conditionTable)
        group = item.parent()
        group.insertLayer(group.children().index(item), self.conditionLayer)

    def onSelectFeature(self):
        if super().onSelectFeature():
            # Returning True from onSelectFeature() means that the feature was newly selected.
            self.addConditionLayer()
            return True
        return False

    def onDeselectFeature(self):
        if super().onDeselectFeature():
            # Returning False from onDeselectFeature() means that the feature was newly deselected.
            try:
                if self.conditionLayer:
                    layer = QgsProject.instance().layerTreeRoot().findLayer(self.conditionLayer)
                    if layer:
                        layer.parent().removeChildNode(layer)
                    self.conditionLayer = None
            except BaseException:
                pass
            finally:
                return True
        return False

    # @Glitch.glitchy()
    # def getConditionRecordsForPaddock(self):
    #     paddockRequest = QgsFeatureRequest().setFilterExpression(
    #         f'"{PADDOCK}" = {self.id}')

    #     return list(self.conditionRecordLayer.getFeatures(paddockRequest))

    # @Glitch.glitchy()
    # def analyseConditionRecords(self):
    #     """Get the land systems that intersect this paddock."""

    #     landSystems = (self.landSystemLayer.getFeatures(self.geometry.boundingBox()))
    #     near, far = self.waterpointBufferLayer.getNearAndFarBuffers()

    #     overLandSystems = [record
    #                        for landSystem in landSystems if landSystem.geometry.intersects(self.geometry)
    # for record in
    # OldConditionRecord.fromPaddockAndLandSystem(self.conditionRecordLayer,
    # self, landSystem)]

    #     overNearBuffer = [record for unwatered in overLandSystems
    #                       for record in unwatered.overWaterpointBuffer(near)]

    #     overFarBuffer = [record for unwatered in overLandSystems
    #                      for record in unwatered.overWaterpointBuffer(far)]

    #     return (overNearBuffer + overFarBuffer), self.getConditionRecordsForPaddock()

    # def analyseFeature(self):
    #     """Analyse the feature."""
    #     super().recalculate() # Re-check the area and perimeter

    #     edits = Edits()

    #     conditionRecords, currentConditionRecords = self.analyseConditionRecords()

    #     for record in conditionRecords:
    #         record.recalculate()

    #     self.estimatedCapacity = sum([record.estimatedCapacity for record in conditionRecords])
    #     self.potentialCapacity = sum([record.potentialCapacity for record in conditionRecords])
    #     self.capacityPerArea = self.estimatedCapacity / self.featureArea

    #     edits.editBefore(Edits.delete(*currentConditionRecords))
    #     edits.editBefore(Edits.upsert(*conditionRecords))
    #     return edits

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
