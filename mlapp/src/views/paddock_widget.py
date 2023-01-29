# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ..spatial.layers.feature_layer import FeatureLayer


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_widget_base.ui')))


class PaddockWidget(QWidget, FORM_CLASS):

    def __init__(self, workspace, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.workspace = workspace

        self.setupUi(self)

        self.paddockList.paddockLayer = self.workspace.paddockLayer
        self.paddockList.setFeatureLayer(self.workspace.derivedMetricPaddockLayer)

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

    @pyqtSlot(FeatureLayer)
    def setPaddockLandTypesLayer(self, layer=None):
        self.paddockLandTypeList.setFeatureLayer(layer)

    @pyqtSlot()
    def clearPaddockLandTypesLayer(self):
        self.paddockLandTypeList.setFeatureLayer(None)

    def onPaddockFilterChanged(self, text):
        self.paddockList.filterByName(text)
