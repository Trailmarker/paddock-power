# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from qgis.core import QgsProject

from ...spatial.features.feature import Feature
from ...spatial.features.paddock import Paddock
from ...spatial.layers.metric_paddock_popup_layer import MetricPaddockPopupLayer
from .paddock_list_item import PaddockListItem
from .persisted_feature_layer_list import PersistedFeatureLayerList


class PaddockLayerList(PersistedFeatureLayerList):

    popupLayerAdded = pyqtSignal(MetricPaddockPopupLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""

        self._derivedMetricPaddockLayerId = None

        def listItemFactory(paddock):
            return PaddockListItem(paddock, self.derivedMetricPaddockLayer, parent=parent)

        super().__init__(listItemFactory, parent)

    @property
    def derivedMetricPaddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId) if self._derivedMetricPaddockLayerId else None

    @derivedMetricPaddockLayer.setter
    def derivedMetricPaddockLayer(self, derivedMetricPaddockLayer):
        """Set the FeatureLayer."""
        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id() if derivedMetricPaddockLayer else None

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, feature):
        """Handle changes to the selected Feature in the underlying Featureayer."""
        super().onSelectedFeatureChanged(feature)

        if isinstance(feature, Paddock):
            feature.popupLayerAdded.connect(self.onPopupLayerAdded)
            feature.popupLayerRemoved.connect(self.onPopupLayerRemoved)
            self.onPopupLayerAdded(feature.popupLayer)

    @pyqtSlot(MetricPaddockPopupLayer)
    def onPopupLayerAdded(self, layer):
        if layer:
            self.popupLayerAdded.emit(layer)

    @pyqtSlot()
    def onPopupLayerRemoved(self):
        self.popupLayerRemoved.emit()
