# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from qgis.core import QgsProject

from ...spatial.features.paddock import Paddock
from .paddock_list_item import PaddockListItem
from .persisted_feature_layer_list import PersistedFeatureLayerList


class PaddockLayerList(PersistedFeatureLayerList):

    popupLayerAdded = pyqtSignal(MetricPaddockLandTypesPopupLayer)
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

    @pyqtSlot(type, list)
    def onSelectedFeaturesChanged(self, featureLayerType, features):
        """Handle changes to the selected Feature in the underlying Featureayer."""
        super().onSelectedFeaturesChanged(features)
        feature = features[0] if features else None
        if isinstance(feature, Paddock):
            feature.popupLayerAdded.connect(self.onPopupLayerAdded)
            feature.popupLayerRemoved.connect(self.onPopupLayerRemoved)
            self.onPopupLayerAdded(feature.popupLayer)

    @pyqtSlot(MetricPaddockLandTypesPopupLayer)
    def onPopupLayerAdded(self, layer):
        if layer:
            self.popupLayerAdded.emit(layer)

    @pyqtSlot()
    def onPopupLayerRemoved(self):
        self.popupLayerRemoved.emit()
