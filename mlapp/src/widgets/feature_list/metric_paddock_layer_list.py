# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from qgis.core import QgsProject

from ...spatial.features.feature import Feature
from ...spatial.features.paddock import MetricPaddock
from ...spatial.layers.paddock_land_types_popup_layer import PaddockLandTypesPopupLayer
from .feature_layer_list import FeatureLayerList
from .metric_paddock_list_item import MetricPaddockListItem


class MetricPaddockLayerList(FeatureLayerList):

    popupLayerAdded = pyqtSignal(PaddockLandTypesPopupLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""

        self._paddockLayerId = None

        def listItemFactory(metricPaddock):
            return MetricPaddockListItem(metricPaddock, self.paddockLayer, parent=parent)

        super().__init__(listItemFactory, parent)

    @property
    def paddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._paddockLayerId) if self._paddockLayerId else None

    @paddockLayer.setter
    def paddockLayer(self, paddockLayer):
        """Set the FeatureLayer."""
        self._paddockLayerId = paddockLayer.id() if paddockLayer else None

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, feature):
        """Handle changes to the selected Feature in the underlying Featureayer."""
        super().onSelectedFeatureChanged(feature)

        if isinstance(feature, MetricPaddock):
            feature.popupLayerAdded.connect(self.onPopupLayerAdded)
            feature.popupLayerRemoved.connect(self.onPopupLayerRemoved)
            self.onPopupLayerAdded(feature.popupLayer)

    @pyqtSlot(PaddockLandTypesPopupLayer)
    def onPopupLayerAdded(self, layer):
        if layer:
            self.popupLayerAdded.emit(layer)

    @pyqtSlot()
    def onPopupLayerRemoved(self):
        self.popupLayerRemoved.emit()
