# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from ...features.feature import Feature
from ..feature_layer import FeatureLayer


class PopupFeatureLayerMixin:

    popupLayerAdded = pyqtSignal(FeatureLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot(FeatureLayer)
    def onPopupLayerAdded(self, layer):
        if layer:
            self.popupLayerAdded.emit(layer)

    @pyqtSlot()
    def onPopupLayerRemoved(self):
        self.popupLayerRemoved.emit()
