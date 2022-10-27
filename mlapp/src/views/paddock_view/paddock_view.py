# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot

from ...spatial.layers.derived_layer import DerivedLayer
from ...utils import qgsDebug
from ..view_base import ViewBase

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_view_base.ui')))


class PaddockView(ViewBase, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(project, parent)

        self.setupUi(self)

        self.paddockList.featureLayer = self.project.paddockLayer

        self.paddockList.popupLayerAdded.connect(self.setConditionLayer)
        self.paddockList.popupLayerRemoved.connect(self.clearConditionLayer)

        self.paddockFilterLineEdit.textChanged.connect(
            self.onPaddockFilterChanged)
        self.clearPaddockFilterButton.clicked.connect(
            self.paddockFilterLineEdit.clear)

    @pyqtSlot(DerivedLayer)
    def setConditionLayer(self, layer=None):
        qgsDebug(f"PaddockView.setConditionLayer({layer.__class__.__name__})")
        self.conditionList.featureLayer = layer

    @pyqtSlot()
    def clearConditionLayer(self):
        qgsDebug(f"PaddockView.unsetConditionLayer()")
        self.conditionList.featureLayer = None

    def onPaddockFilterChanged(self, text):
        self.paddockList.filterByName(text)
