# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsFeatureRequest, QgsProject

from ...utils import qgsInfo, randomString
from ..layers.condition_table import ConditionTable
from ..layers.land_system_layer import LandSystemLayer
from ..layers.paddock_land_systems_popup_layer import PaddockLandSystemsPopupLayer
from ..layers.derived_watered_area_layer import DerivedWateredAreaLayer
from ..schemas.schemas import PaddockSchema
from .area_feature import AreaFeature
from .edits import Edits
from .feature_action import FeatureAction


@PaddockSchema.addSchema()
class Paddock(AreaFeature):

    popupLayerAdded = pyqtSignal(PaddockLandSystemsPopupLayer)
    popupLayerRemoved = pyqtSignal()

    @classmethod
    def twoPhaseRecalculate(self):
        return True

    def __init__(self, featureLayer, landSystemLayer: LandSystemLayer, wateredAreaLayer: DerivedWateredAreaLayer,
                 conditionTable: ConditionTable, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature=existingFeature)

        self._landSystemLayerId = landSystemLayer.id()
        self._wateredAreaLayerId = wateredAreaLayer.id()
        self.conditionTable = conditionTable

        self._popupLayerId = None
        self._recalculateLayerId = None

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def wateredAreaLayer(self):
        return QgsProject.instance().mapLayer(self._wateredAreaLayerId)

    @property
    def popupLayer(self):
        return QgsProject.instance().mapLayer(self._popupLayerId) if self._popupLayerId else None

    @popupLayer.setter
    def popupLayer(self, popupLayer):
        self._popupLayerId = popupLayer.id() if popupLayer else None

    @property
    def recalculateLayer(self):
        return QgsProject.instance().mapLayer(self._recalculateLayerId) if self._recalculateLayerId else None

    @recalculateLayer.setter
    def recalculateLayer(self, recalculateLayer):
        self._recalculateLayerId = recalculateLayer.id() if recalculateLayer else None

    def recalculate(self):
        super().recalculate()

        try:
            self.recalculateLayer = PaddockLandSystemsPopupLayer(
                self.featureLayer.getPaddockPowerProject(),
                f"Paddock{self.id}Recalculate{randomString()}",
                self,
                self.featureLayer,
                self.landSystemLayer,
                self.wateredAreaLayer,
                self.conditionTable)

            request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
            paddockLandSystems = [f for f in self.recalculateLayer.getFeatures(request)]

            estimatedRaw = sum([c.estimatedCapacity for c in paddockLandSystems])
            self.estimatedCapacity = round(estimatedRaw, 2)
            potentialRaw = sum([c.potentialCapacity for c in paddockLandSystems])
            self.potentialCapacity = round(potentialRaw, 2)

            self.estimatedCapacityPerArea = round(estimatedRaw / self.featureArea, 2)
            self.potentialCapacityPerArea = round(potentialRaw / self.featureArea, 2)

        except BaseException as e:
            qgsInfo(f"{self}.recalculate() failed with exception {e}")
        finally:
            # Scoping and QGIS layer ownership design mean layer's (usually) already deleted by here
            self.recalculateLayer = None
            # if self.recalculateLayer:
            #     self.recalculateLayer.detectAndRemove()

        qgsInfo(f"{self}.recalculate(): estimatedCapacity={self.estimatedCapacity}, potentialCapacity={self.potentialCapacity}, estimatedCapacityPerArea={self.estimatedCapacityPerArea}, potentialCapacityPerArea={self.potentialCapacityPerArea}")

    def addPopupLayer(self):
        """Add a condition layer to the project."""
        if not self.popupLayer:
            item = QgsProject.instance().layerTreeRoot().findLayer(self.featureLayer)
            if not item:
                # If the Paddocks layer isn't in the map, don't initialise or add the Paddock Land Systems layer.
                return

            # Remove any existing Paddock Land Systems popup layers - they don't play nice together
            PaddockLandSystemsPopupLayer.detectAndRemoveAllOfType()

            self.popupLayer = PaddockLandSystemsPopupLayer(
                self.featureLayer.getPaddockPowerProject(),
                f"{self.name} Land Systems",
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
        """Remove any Paddock Condition popup layer from the project."""
        try:
            if self.popupLayer:
                layer = QgsProject.instance().layerTreeRoot().findLayer(self.popupLayer)
                if layer:
                    layer.setItemVisibilityChecked(False)
                    self.popupLayer.triggerRepaint()
                    layer.parent().removeChildNode(layer)
                    QgsProject.instance().removeMapLayer(self.popupLayer.id())
        except BaseException:
            pass
        finally:
            self.popupLayerRemoved.emit()
            self.popupLayer = None

    def onSelectFeature(self):
        if super().onSelectFeature():
            # Returning True from onSelectFeature() means that the feature was newly selected.
            self.addPopupLayer()
            return True
        return False

    def onDeselectFeature(self):
        if super().onDeselectFeature():
            # Returning True from onDeselectFeature() means that the feature was newly deselected.
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
