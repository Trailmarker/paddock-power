# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from ...spatial.features.feature import Feature
from ...spatial.features.paddock import Paddock
from ...spatial.layers.paddock_land_systems_popup_layer import PaddockLandSystemsPopupLayer
from ..paddock_details.paddock_details import PaddockDetails
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit
from .persisted_feature_collapsible_list_item import PersistedFeatureCollapsibleListItem
from .persisted_feature_layer_list import PersistedFeatureLayerList


class PaddockLayerList(PersistedFeatureLayerList):

    popupLayerAdded = pyqtSignal(PaddockLandSystemsPopupLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddock):
            return PersistedFeatureCollapsibleListItem(paddock, PaddockDetails, PaddockDetailsEdit, self)

        super().__init__(listItemFactory, parent)

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, feature):
        """Handle changes to the selected Feature in the underlying Featureayer."""
        super().onSelectedFeatureChanged(feature)

        if isinstance(feature, Paddock):
            feature.popupLayerAdded.connect(self.onPopupLayerAdded)
            feature.popupLayerRemoved.connect(self.onPopupLayerRemoved)
            self.onPopupLayerAdded(feature.popupLayer)

    @pyqtSlot(PaddockLandSystemsPopupLayer)
    def onPopupLayerAdded(self, layer):
        if layer:
            self.popupLayerAdded.emit(layer)

    @pyqtSlot()
    def onPopupLayerRemoved(self):
        self.popupLayerRemoved.emit()
