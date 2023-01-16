# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ..spatial.layers.paddock_land_types_popup_layer import PaddockLandTypesPopupLayer


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_widget_base.ui')))


class PaddockWidget(QWidget, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.project = project

        self.setupUi(self)

        self.paddockList.derivedMetricPaddockLayer = self.project.derivedMetricPaddockLayer
        self.paddockList.featureLayer = self.project.paddockLayer

        self.splitter.setSizes([self.paddockListGroupBox.sizeHint().width(),
                               self.paddockLandTypeListGroupBox.sizeHint().width()])
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, True)

        self.paddockList.popupLayerAdded.connect(self.setPaddockLandTypesLayer)
        self.paddockList.popupLayerRemoved.connect(self.clearPaddockLandTypesLayer)

        self.paddockFilterLineEdit.textChanged.connect(
            self.onPaddockFilterChanged)
        self.clearPaddockFilterButton.clicked.connect(
            self.paddockFilterLineEdit.clear)

    @pyqtSlot(PaddockLandTypesPopupLayer)
    def setPaddockLandTypesLayer(self, layer=None):
        self.paddockLandTypeList.featureLayer = layer

    @pyqtSlot()
    def clearPaddockLandTypesLayer(self):
        self.paddockLandTypeList.featureLayer = None

    def onPaddockFilterChanged(self, text):
        self.paddockList.filterByName(text)
