# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from ...spatial.layers.derived_feature_layer import DerivedFeatureLayer
from ...utils import qgsDebug
from ..paddock_details.paddock_details import PaddockDetails
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit
from .persisted_feature_collapsible_list_item import PersistedFeatureCollapsibleListItem
from .persisted_feature_layer_list import PersistedFeatureLayerList


class PaddockLayerList(PersistedFeatureLayerList):

    popupLayerAdded = pyqtSignal(DerivedFeatureLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddock):
            paddock.popupLayerAdded.connect(self.onPopupLayerAdded)
            paddock.popupLayerRemoved.connect(self.onPopupLayerRemoved)
            return PersistedFeatureCollapsibleListItem(paddock, PaddockDetails, PaddockDetailsEdit, self)

        super().__init__(listItemFactory, parent)

    @pyqtSlot(DerivedFeatureLayer)
    def onPopupLayerAdded(self, layer):
        # qgsDebug(f"PaddockLayerList.onPopupLayerAdded({layer})")
        self.popupLayerAdded.emit(layer)

    @pyqtSlot()
    def onPopupLayerRemoved(self):
        # qgsDebug(f"PaddockLayerList.onPopupLayerRemoved()")
        self.popupLayerRemoved.emit()
