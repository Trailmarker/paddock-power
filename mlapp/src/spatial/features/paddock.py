# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from ...utils import qgsDebug
from ..layers.condition_table import ConditionTable
from ..layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from ..layers.paddock_land_types_layer import PaddockLandTypesLayer
from ..layers.paddock_land_types_popup_layer import PaddockLandTypesPopupLayer
from ..fields.schemas import PaddockSchema
from .area_feature import AreaFeature
from .edits import Edits
from .feature_action import FeatureAction


@PaddockSchema.addSchema()
class Paddock(AreaFeature):

    popupLayerAdded = pyqtSignal(PaddockLandTypesPopupLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, featureLayer, derivedMetricPaddockLayer: DerivedMetricPaddockLayer,
                 paddockLandTypesLayer: PaddockLandTypesLayer, conditionTable: ConditionTable, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature=existingFeature)

        self.crossedPaddockId = None

        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id()
        self._paddockLandTypesLayerId = paddockLandTypesLayer.id()
        self.conditionTable = conditionTable

        self._popupLayerId = None

    @property
    def title(self):
        return f"{self.name} ({self.featureArea:.2f} km²)"

    @property
    def derivedMetricPaddockLayer(self):
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId)

    @property
    def paddockLandTypesLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLandTypesLayerId)

    @property
    def popupLayer(self):
        return QgsProject.instance().mapLayer(self._popupLayerId) if self._popupLayerId else None

    @popupLayer.setter
    def popupLayer(self, popupLayer):
        self._popupLayerId = popupLayer.id() if popupLayer else None

    def upsert(self):
        """Upsert the Paddock and also upsert a Condition record if the Paddock has been split."""    
        super().upsert()

        if self.crossedPaddockId:
            # qgsDebug(f"{self}.conditionTable.upsertSplit({self.id}, {self.crossedPaddockId})")
            self.conditionTable.upsertSplit(self.id, self.crossedPaddockId)

        self.featureUpserted.emit()
        return self.id

    def addPopupLayer(self):
        """Add a condition layer to the project."""
        if not self.popupLayer:
            item = QgsProject.instance().layerTreeRoot().findLayer(self.derivedMetricPaddockLayer)
            if not item:
                # If the Metric Paddocks layer isn't in the map, don't initialise or add the Paddock Land Types layer.
                return

            # Remove any existing Paddock Land Types popup layers - they don't play nice together
            PaddockLandTypesPopupLayer.detectAndRemoveAllOfType()

            self.popupLayer = PaddockLandTypesPopupLayer(
                self.featureLayer.getPaddockPowerProject(),
                f"{self.name} Land Types",
                self,
                self.paddockLandTypesLayer,
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
        """Do the stuff we'd normally do, but also add the Paddock Land Types popup layer."""
        super().onSelectFeature()
        # qgsDebug(f"{self}.onSelectFeature()")
        self.addPopupLayer()

    def onDeselectFeature(self):
        """Do the stuff we'd normally do, but also remove the Paddock Land Types popup layer."""
        super().onDeselectFeature()
        self.removePopupLayer()

    @FeatureAction.draft.handler()
    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        self.name = name
        self.geometry = geometry
        return Edits.upsert(self)

    @FeatureAction.plan.handler()
    def planFeature(self, fence, crossedPaddock=None):
        self.buildFence = fence.buildOrder
        self.crossedPaddockId = crossedPaddock.id if crossedPaddock else None
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
