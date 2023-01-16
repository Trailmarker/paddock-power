# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from ...utils import qgsDebug
from ..layers.condition_table import ConditionTable
from ..layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from ..layers.paddock_land_types_layer import PaddockLandSystemsLayer
from ..layers.paddock_land_types_popup_layer import PaddockLandSystemsPopupLayer
from ..fields.schemas import PaddockSchema
from .area_feature import AreaFeature
from .edits import Edits
from .feature_action import FeatureAction


@PaddockSchema.addSchema()
class Paddock(AreaFeature):

    popupLayerAdded = pyqtSignal(PaddockLandSystemsPopupLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, featureLayer, derivedMetricPaddockLayer: DerivedMetricPaddockLayer,
                 paddockLandSystemsLayer: PaddockLandSystemsLayer, conditionTable: ConditionTable, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature=existingFeature)

        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id()
        self._paddockLandSystemsLayerId = paddockLandSystemsLayer.id()
        self.conditionTable = conditionTable

        self._popupLayerId = None

    @property
    def title(self):
        return f"{self.name} ({self.featureArea:.2f} km²)"

    @property
    def derivedMetricPaddockLayer(self):
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId)

    @property
    def paddockLandSystemsLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLandSystemsLayerId)

    @property
    def popupLayer(self):
        return QgsProject.instance().mapLayer(self._popupLayerId) if self._popupLayerId else None

    @popupLayer.setter
    def popupLayer(self, popupLayer):
        self._popupLayerId = popupLayer.id() if popupLayer else None

    def addPopupLayer(self):
        """Add a condition layer to the project."""
        if not self.popupLayer:
            item = QgsProject.instance().layerTreeRoot().findLayer(self.derivedMetricPaddockLayer)
            if not item:
                # If the Metric Paddocks layer isn't in the map, don't initialise or add the Paddock Land Systems layer.
                return

            # Remove any existing Paddock Land Systems popup layers - they don't play nice together
            PaddockLandSystemsPopupLayer.detectAndRemoveAllOfType()

            self.popupLayer = PaddockLandSystemsPopupLayer(
                self.featureLayer.getPaddockPowerProject(),
                f"{self.name} Land Systems",
                self,
                self.paddockLandSystemsLayer,
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
        """Do the stuff we'd normally do, but also add the Paddock Land Systems popup layer."""
        super().onSelectFeature()
        # qgsDebug(f"{self}.onSelectFeature()")
        self.addPopupLayer()

    def onDeselectFeature(self):
        """Do the stuff we'd normally do, but also remove the Paddock Land Systems popup layer."""
        super().onDeselectFeature()
        self.removePopupLayer()

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
