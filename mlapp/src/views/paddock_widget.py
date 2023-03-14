# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtWidgets import QWidget

from ..layers import PopupLayerConsumerMixin, PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer
from ..models import WorkspaceMixin, Glitch
from ..utils import qgsDebug
from ..widgets.feature_table.paddock_land_types_table import CurrentPaddockLandTypesTable, FuturePaddockLandTypesTable

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_widget_base.ui')))


class PaddockWidget(QWidget, FORM_CLASS, WorkspaceMixin, PopupLayerConsumerMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.layoutTimer = QTimer()
        self.layoutTimer.setSingleShot(True)
        self.layoutTimer.setInterval(100)
        self.layoutTimer.timeout.connect(lambda: self.relayout())

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, False)
        self.splitter.setCollapsible(3, True)

        self.popupLayerSource = self.workspace.paddockLayer

        self.showingCurrentPopup = False
        self.currentPaddockLandTypesTable = None
        self.showingFuturePopup = False
        self.futurePaddockLandTypesTable = None

    def resizeEvent(self, event):
        """Override in subclass to handle resize event."""
        super().resizeEvent(event)

        # Re-start the timeout while we're resizing
        self.layoutTimer.stop()
        self.layoutTimer.start()

    def relayout(self):
        self.splitter.setSizes([self.paddockTable.sizeHint().width() +6,
                                self.currentPaddockLandTypesTable.sizeHint().width() + 6 if self.showingCurrentPopup else 0,
                                self.futurePaddockLandTypesTable.sizeHint().width() + 6 if self.showingFuturePopup else 0,
                                self.spacerWidget.sizeHint().width()])

    @property
    def popupLayerTypes(self):
        """Popup layer types that this layer can consume."""
        return [PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer]

    @property
    def popupLayer(self, layerType):
        """Get the current popup layer of the given type."""
        if layerType != self.popupLayerType:
            raise Glitch("Unexpected layer type: %s" % layerType)

    def onPopupLayerAdded(self, layerId):
        """Override in subclass to handle popup layer added."""
        featureLayer = self.workspace.mapLayer(layerId)

        if type(featureLayer) not in self.popupLayerTypes:
            qgsDebug(f"{type(self).__name__}.onPopupLayerAdded({layerId}) - not supported")
            return

        if isinstance(featureLayer, PaddockCurrentLandTypesPopupLayer):
            self.currentPaddockLandTypesTable = CurrentPaddockLandTypesTable(self)
            self.currentPaddockLandTypesTableGroupBox.layout().addWidget(self.currentPaddockLandTypesTable)
            self.currentPaddockLandTypesTable.featureLayer = featureLayer
            self.showingCurrentPopup = True

        if isinstance(featureLayer, PaddockFutureLandTypesPopupLayer):
            self.futurePaddockLandTypesTable = FuturePaddockLandTypesTable(self)
            self.futurePaddockLandTypesTableGroupBox.layout().addWidget(self.futurePaddockLandTypesTable)
            self.futurePaddockLandTypesTable.featureLayer = featureLayer
            self.showingFuturePopup = True
            
        self.relayout()

    def onPopupLayerRemoved(self):
        """Override in subclass to handle popup layer removed."""
        if self.currentPaddockLandTypesTable:
            self.showingCurrentPopup = False
            self.currentPaddockLandTypesTableGroupBox.layout().removeWidget(self.currentPaddockLandTypesTable)
            self.currentPaddockLandTypesTable.deleteLater()
            self.currentPaddockLandTypesTable = None
        if self.futurePaddockLandTypesTable:
            self.showingFuturePoup = False
            self.futurePaddockLandTypesTableGroupBox.layout().removeWidget(self.futurePaddockLandTypesTable)
            self.futurePaddockLandTypesTable.deleteLater()
            self.futurePaddockLandTypesTable = None
