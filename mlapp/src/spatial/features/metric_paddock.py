# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from ..fields.schemas import MetricPaddockSchema
from ..layers.paddock_land_types_popup_layer import PaddockLandTypesPopupLayer
from .status_feature import StatusFeature


@MetricPaddockSchema.addSchema()
class MetricPaddock(StatusFeature):

    popupLayerAdded = pyqtSignal(PaddockLandTypesPopupLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, featureLayer, paddockLandTypesLayer, conditionTable, existingFeature=None):
        """Initialise a new Metric Paddock."""
        super().__init__(featureLayer=featureLayer, existingFeature=existingFeature)

        self._paddockLandTypesLayerId = paddockLandTypesLayer.id()
        self.conditionTable = conditionTable

        self._popupLayerId = None

    @property
    def title(self):
        return f"{self.name} ({self.featureArea:.2f} km²)"

    @property
    def paddockLandTypesLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLandTypesLayerId)

    @property
    def popupLayer(self):
        return QgsProject.instance().mapLayer(self._popupLayerId) if self._popupLayerId else None

    @popupLayer.setter
    def popupLayer(self, popupLayer):
        self._popupLayerId = popupLayer.id() if popupLayer else None

    def addPopupLayer(self):
        """Add a condition layer to the project."""
        if not self.popupLayer:
            item = QgsProject.instance().layerTreeRoot().findLayer(self.featureLayer)
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
