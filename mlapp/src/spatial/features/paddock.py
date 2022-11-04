# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsFeatureRequest, QgsProject

from ...utils import qgsInfo
from ..layers.condition_table import ConditionTable
from ..layers.derived_layer import DerivedLayer
from ..layers.land_system_layer import LandSystemLayer
from ..layers.paddock_condition_popup_layer import PaddockConditionPopupLayer
from ..layers.watered_area_layer import WateredAreaLayer
from ..schemas.schemas import PaddockSchema
from .area_feature import AreaFeature
from .edits import Edits
from .feature_action import FeatureAction


@PaddockSchema.addSchema()
class Paddock(AreaFeature):

    popupLayerAdded = pyqtSignal(DerivedLayer)
    popupLayerRemoved = pyqtSignal()

    @classmethod
    def twoPhaseRecalculate(self):
        return True

    def __init__(self, featureLayer, landSystemLayer: LandSystemLayer, wateredAreaLayer: WateredAreaLayer,
                 conditionTable: ConditionTable, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature=existingFeature)

        self._landSystemLayerId = landSystemLayer.id()
        self._wateredAreaLayerId = wateredAreaLayer.id()
        self.conditionTable = conditionTable

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def wateredAreaLayer(self):
        return QgsProject.instance().mapLayer(self._wateredAreaLayerId)

    @property
    def conditionRecordLayer(self):
        return QgsProject.instance().mapLayer(self._conditionRecordLayerId)

    def recalculate(self):
        super().recalculate()

        recalculator = None
        try:
            recalculator = PaddockConditionPopupLayer(
                f"Paddock {self.id} Recalculate",
                self,
                self.featureLayer,
                self.landSystemLayer,
                self.wateredAreaLayer,
                self.conditionTable)

            request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
            conditions = [f for f in recalculator.getFeatures(request)]

            estimatedRaw = sum([c.estimatedCapacity for c in conditions])
            self.estimatedCapacity = round(estimatedRaw)
            self.potentialCapacity = round(sum([c.potentialCapacity for c in conditions]))
            self.capacityPerArea = round(estimatedRaw / self.featureArea, 2)
        except BaseException as e:
            qgsInfo(f"{self}.recalculate() failed with exception {e}")
        finally:
            if recalculator:
                recalculator.detectAndRemove()

        # qgsDebug(f"{self}.recalculate(): estimatedCapacity={self.estimatedCapacity}, potentialCapacity={self.potentialCapacity}, capacityPerArea={self.capacityPerArea}")

    def addPopupLayer(self):
        """Add a condition layer to the project."""
        item = QgsProject.instance().layerTreeRoot().findLayer(self.featureLayer)
        if not item:
            # If the Paddocks layer isn't in the map, don't initialise or add the condition layer.
            return
        self.popupLayer = PaddockConditionPopupLayer(
            f"{self.name} Paddock Condition",
            self,
            self.featureLayer,
            self.landSystemLayer,
            self.wateredAreaLayer,
            self.conditionTable)
        group = item.parent()

        # Bit of a hack but it looks nicer if it's above the derived Boundary layer …
        group.insertLayer(max(0, group.children().index(item) - 1), self.popupLayer)
        self.popupLayerAdded.emit(self.popupLayer)

    def removePopupLayer(self):
        try:
            if self.popupLayer:
                layer = QgsProject.instance().layerTreeRoot().findLayer(self.popupLayer)
                if layer:
                    layer.parent().removeChildNode(layer)
                    QgsProject.instance().removeMapLayer(self.popupLayer.id())
                self.popupLayer = None
                self.popuplayerRemoved.emit()
        except BaseException:
            pass

    def onSelectFeature(self):
        if super().onSelectFeature():
            # Returning True from onSelectFeature() means that the feature was newly selected.
            self.addPopupLayer()
            return True
        return False

    def onDeselectFeature(self):
        if super().onDeselectFeature():
            # Returning False from onDeselectFeature() means that the feature was newly deselected.
            self.removePopupLayer()
            return True
        return False

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
