# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from ..layers.waterpoint_popup_layer import WaterpointPopupLayer
from .edits import Edits
from .feature_action import FeatureAction
from .point_feature import PointFeature
from ..schemas.schemas import WaterpointSchema


@WaterpointSchema.addSchema()
class Waterpoint(PointFeature):

    NEAREST_GRAZING_RADIUS = 0
    FARTHEST_GRAZING_RADIUS = 20000

    popupLayerAdded = pyqtSignal(WaterpointPopupLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, featureLayer, waterpointBufferLayer, elevationLayer=None, existingFeature=None):
        """Create a new LineFeature."""
        super().__init__(featureLayer=featureLayer, elevationLayer=elevationLayer, existingFeature=existingFeature)
        self._waterpointBufferLayerId = waterpointBufferLayer.id()

        self._popupLayerId = None

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId)

    @property
    def popupLayer(self):
        return QgsProject.instance().mapLayer(self._popupLayerId) if self._popupLayerId else None

    @popupLayer.setter
    def popupLayer(self, popupLayer):
        self._popupLayerId = popupLayer.id() if popupLayer else None

    @property
    def title(self):
        if self.name and self.name != "NULL":
            return f"{self.name} ({self.waterpointType})"
        return f"Waterpoint ({self.id}) ({self.waterpointType})"

    def addPopupLayer(self):
        """Add a Waterpoint popup layer to the project."""
        if not self.popupLayer:
            item = QgsProject.instance().layerTreeRoot().findLayer(self.featureLayer)
            if not item:
                # If the Paddocks layer isn't in the map, don't initialise or add the condition layer.
                return

            WaterpointPopupLayer.detectAndRemoveAllOfType()

            self.popupLayer = WaterpointPopupLayer(
                self.featureLayer.getPaddockPowerProject(),
                f"{self.waterpointType.value} {self.id} Watered Area",
                self,
                self.waterpointBufferLayer)
            group = item.parent()
            # Insert the buffers layer immediately below this waterpoint, so it and any neighbouring waterpoints
            # remain visible.
            group.insertLayer(group.children().index(item) + 1, self.popupLayer)

            self.popupLayerAdded.emit(self.popupLayer)

    def removePopupLayer(self):
        """Remove any Waterpoint popup layer from the project."""
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
            self.popupLayer = None
            self.popupLayerRemoved.emit()

    def onSelectFeature(self):
        """Do the stuff we'd normally do, but also add the Waterpoint popup layer."""
        super().onSelectFeature()
        self.addPopupLayer()

    def onDeselectFeature(self):
        """Do the stuff we'd normally do, but also remove the Waterpoint popup layer."""
        super().onDeselectFeature()
        self.removePopupLayer()

    @Edits.persistFeatures
    @FeatureAction.draft.handler()
    def draftFeature(self, point):
        """Draft a Waterpoint."""
        self.geometry = point

        return Edits.upsert(self)
