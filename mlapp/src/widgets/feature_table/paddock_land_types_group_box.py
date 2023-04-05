# -*- coding: utf-8 -*-
from .feature_table_group_box import FeatureTableGroupBox

from ..details import PaddockDetails


class PaddockLandTypesGroupBox(FeatureTableGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.paddockDetails = None

    def removePaddockDetails(self):
        """Remove any current FeatureTable from the widget."""
        if self.paddockDetails:
            self.layout().removeWidget(self.paddockDetails)
            self.paddockDetails.deleteLater()

    def onPopupLayerAdded(self, layerId):
        """Handle a new layer from the popup layer source (if any)."""

        featureLayer = self.workspace.mapLayer(layerId)
        if type(featureLayer) not in self.popupLayerTypes:
            return

        # feature layer is a subclass of PaddockLandTypesPopupLayer
        self.removePaddockDetails()
        self.paddockDetails = PaddockDetails(featureLayer.paddock, self)
        self.layout().addWidget(self.paddockDetails)

        # set the feature layer (triggers other logic)
        self.featureLayer = featureLayer

    def onPopupLayerRemoved(self):
        """Override in subclass to handle popup layer removed."""
        self.featureLayer = None
