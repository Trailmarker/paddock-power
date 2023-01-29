# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from ..fields.schemas import MetricPaddockSchema
from ..layers.metric_paddock_popup_layer import MetricPaddockPopupLayer
from ..layers.paddock_layer import PaddockLayer
from ..layers.paddock_land_types_layer import PaddockLandTypesLayer
from .feature_action import FeatureAction
from .status_feature import StatusFeature


@MetricPaddockSchema.addSchema()
class MetricPaddock(StatusFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Metric Paddock."""
        super().__init__(featureLayer, existingFeature)

        self._popupLayerId = None

    @property
    def TITLE(self):
        return f"{self.NAME} ({self.AREA:.2f} km²)"

    @property
    def paddockLayer(self):
        return self.depend(PaddockLayer)

    @property
    def paddockLandTypesLayer(self):
        return self.depend(PaddockLandTypesLayer)

    @property
    def popupLayer(self):
        return QgsProject.instance().mapLayer(self._popupLayerId) if self._popupLayerId else None

    @popupLayer.setter
    def popupLayer(self, popupLayer):
        self._popupLayerId = popupLayer.id() if popupLayer else None

    def addPopupLayer(self):
        """Add a Metrick Paddock popup layer."""
        if not self.popupLayer:
            item = QgsProject.instance().layerTreeRoot().findLayer(self.featureLayer)
            if not item:
                # If the Metric Paddocks layer isn't in the map, don't initialise or add the Paddock Land Types layer.
                return

            # Remove any existing Paddock Land Types popup layers - they don't play nice together
            MetricPaddockPopupLayer.detectAndRemoveAllOfType()

            self.popupLayer = MetricPaddockPopupLayer(
                self.featureLayer.getPaddockPowerProject(),
                f"{self.NAME} Land Types",
                self,
                self.paddockLandTypesLayer,
                self.conditionTable)

            group = item.parent()

            # Bit of a hack but it looks nicer if it's above the derived Boundary layer …
            group.insertLayer(max(0, group.children().index(item) - 1), self.popupLayer)

            self.popupLayerAdded.emit(self.popupLayer)

    def removePopupLayer(self):
        """Remove any Metric Paddock popup layer."""
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

    # All workflow functions are deferred to the underlying Paddock for this MetricPaddock
    def getPaddock(self):
        """Get the Paddock that this Metric Paddock is associated with."""
        return self.paddockLayer.getFeature(self.paddock)

    @FeatureAction.draft.handler()
    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        return self.getPaddock().draftFeature(geometry, name)

    @FeatureAction.plan.handler()
    def planFeature(self, fence, crossedPaddock=None):
        return self.getPaddock().planFeature(fence, crossedPaddock)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        return self.getPaddock().undoPlanFeature()

    @FeatureAction.supersede.handler()
    def supersedeFeature(self, fence):
        return self.getPaddock().supersedeFeature(fence)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        return self.getPaddock().undoSupersedeFeature()
