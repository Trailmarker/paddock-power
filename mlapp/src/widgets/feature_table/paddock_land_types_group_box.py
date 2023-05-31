# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from ...utils import PLUGIN_FOLDER
from ..details import PaddockDetails
from .feature_table_group_box import FeatureTableGroupBox


class PaddockLandTypesGroupBox(FeatureTableGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create and add an empty PaddockDetails
        self.paddockDetails = PaddockDetails(None, self)

        # Set up a tool to extract the CSV of the Paddock
        extractCsvIcon = QIcon(f":/plugins/{PLUGIN_FOLDER}/images/extract-csv.png")
        extractCsvAction = QAction(extractCsvIcon, "Extract CSV …", self)
        extractCsvAction.triggered.connect(lambda *_: self.extractCsv())
        self.paddockDetails.addAction(extractCsvAction)

        self.layout().insertWidget(0, self.paddockDetails)

        # If we've got PaddockDetails, update display when paddocks are updated
        self.workspace.paddockLayer.editsPersisted.connect(self.onPaddocksUpdated)

    def onPaddocksUpdated(self):
        """Update the PaddockDetails display."""
        # If there's no data, clear the PaddockDetails model
        showData = bool(self.featureLayer) and self.featureLayer.featureCount() > 0
        self.paddockDetails.model = self.featureLayer.paddock if showData else None

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

    def extractCsv(self):
        """Extract a CSV representation of the current Paddock Land Types layer loaded in this widget."""
        if self.featureLayer:
            self.featureLayer.extractCsv()
