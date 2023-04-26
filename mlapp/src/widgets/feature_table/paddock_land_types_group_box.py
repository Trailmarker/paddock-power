# -*- coding: utf-8 -*-
from .feature_table_group_box import FeatureTableGroupBox

from ..details import PaddockDetails


class PaddockLandTypesGroupBox(FeatureTableGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.paddockDetails = None

        # If we've got PaddockDetails, update display when paddocks are updated
        self.workspace.paddockLayer.editsPersisted.connect(self.onPaddocksUpdated)

    def onPaddocksUpdated(self):
        """Update the PaddockDetails display."""
        if self.featureLayer:
            if not self.paddockDetails:
                # Create and add the PaddockDetails
                self.paddockDetails = PaddockDetails(self.featureLayer.paddock, self)
                self.layout().addWidget(self.paddockDetails)
            else:
                # Just update the PaddockDetails display
                self.paddockDetails.model = self.featureLayer.paddock

    def onPopupLayerAdded(self, layerId):
        """Handle a new layer from the popup layer source (if any)."""

        featureLayer = self.workspace.mapLayer(layerId)
        if type(featureLayer) not in self.popupLayerTypes:
            return
        
        # Trigger the default logic for handling a new feature layer
        self.featureLayer = featureLayer

        self.onPaddocksUpdated()

    def onPopupLayerRemoved(self):
        """Override in subclass to handle popup layer removed."""
        self.featureLayer = None
