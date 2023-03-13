# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ..layers import PopupLayerConsumerMixin, PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer
from ..models import WorkspaceMixin, Glitch
from ..utils import qgsDebug
from ..widgets.feature_table_view.paddock_land_types_table_view import CurrentPaddockLandTypesTableView, FuturePaddockLandTypesTableView

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_widget_base.ui')))


class PaddockWidget(QWidget, FORM_CLASS, WorkspaceMixin, PopupLayerConsumerMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, False)
        self.splitter.setCollapsible(3, True)

        self.popupLayerSource = self.workspace.paddockLayer

        self.currentPaddockLandTypesTableView = None
        self.futurePaddockLandTypesTableView = None

        # self.currentPaddockLandTypesTableView.popupLayerSource = self.workspace.paddockLayer
        # self.futurePaddockLandTypesTableView.popupLayerSource = self.workspace.paddockLayer

        # self.paddockFilterLineEdit.textChanged.connect(
        #     self.onPaddockFilterChanged)
        # self.clearPaddockFilterButton.clicked.connect(
        #     self.paddockFilterLineEdit.clear)

    # def onPaddockFilterChanged(self, text):
    #     self.paddockList.filterByName(text)

    @property
    def popupLayerTypes(self):
        """Popup layer types that this layer can consume."""
        return [PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer]

    @property
    def popupLayer(self, layerType):
        """Get the current popup layer of the given type."""
        if layerType != self.popupLayerType:
            raise Glitch("Unexpected layer type: %s" % layerType)

    def refreshUi(self):
        pass

    def onPopupLayerAdded(self, layerId):
        """Override in subclass to handle popup layer added."""
        featureLayer = self.workspace.mapLayer(layerId)

        if type(featureLayer) not in self.popupLayerTypes:
            qgsDebug(f"{type(self).__name__}.onPopupLayerAdded({layerId}) - not supported")
            return
        
        if type(featureLayer) == PaddockCurrentLandTypesPopupLayer:
            self.currentPaddockLandTypesTableView = CurrentPaddockLandTypesTableView(self)
            self.currentPaddockLandTypesTableViewGroupBox.layout().addWidget(self.currentPaddockLandTypesTableView)
            self.currentPaddockLandTypesTableView.featureLayer = featureLayer

        if type(featureLayer) == PaddockFutureLandTypesPopupLayer:
            self.futurePaddockLandTypesTableView = FuturePaddockLandTypesTableView(self)
            self.futurePaddockLandTypesTableViewGroupBox.layout().addWidget(self.futurePaddockLandTypesTableView)
            self.futurePaddockLandTypesTableView.featureLayer = featureLayer         

    def onPopupLayerRemoved(self):
        """Override in subclass to handle popup layer removed."""
        if self.currentPaddockLandTypesTableView:
            self.currentPaddockLandTypesTableViewGroupBox.layout().removeWidget(self.currentPaddockLandTypesTableView)
            self.currentPaddockLandTypesTableView.deleteLater()
            self.currentPaddockLandTypesTableView = None
        if self.futurePaddockLandTypesTableView:
            self.futurePaddockLandTypesTableViewGroupBox.layout().removeWidget(self.futurePaddockLandTypesTableView)
            self.futurePaddockLandTypesTableView.deleteLater()
            self.futurePaddockLandTypesTableView = None

