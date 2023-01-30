# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ..spatial.fields.timeframe import Timeframe
from ..spatial.layers.metric_paddock_land_types_popup_layer import MetricPaddockCurrentLandTypesPopupLayer, MetricPaddockFutureLandTypesPopupLayer
from ..models.workspace_mixin import WorkspaceMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_widget_base.ui')))


class PaddockWidget(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.splitter.setSizes([self.paddockListGroupBox.sizeHint().width(),
                                self.currentPaddockLandTypeListGroupBox.sizeHint().width(),
                                self.futurePaddockLandTypeListGroupBox.sizeHint().width()])
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, True)

        self.currentPaddockLandTypeList.timeframe = Timeframe.Current
        self.futurePaddockLandTypeList.timeframe = Timeframe.Future

        self.workspace.derivedMetricPaddockLayer.popupLayerAdded.connect(self.setPaddockLandTypesLayer)
        self.workspace.derivedMetricPaddockLayer.popupLayerRemoved.connect(self.clearPaddockLandTypesLayers)

        self.paddockFilterLineEdit.textChanged.connect(
            self.onPaddockFilterChanged)
        self.clearPaddockFilterButton.clicked.connect(
            self.paddockFilterLineEdit.clear)

    def setPaddockLandTypesLayer(self, popupLayer):
        if type(popupLayer) == MetricPaddockCurrentLandTypesPopupLayer:
           self.currentPaddockLandTypeList.featureLayer = popupLayer
        elif type(popupLayer) == MetricPaddockFutureLandTypesPopupLayer:
           self.futurePaddockLandTypeList.featureLayer = popupLayer
        # pass

    @pyqtSlot()
    def clearPaddockLandTypesLayers(self):
        self.currentPaddockLandTypeLsist.featureLayer = None
        self.futurePaddockLandTypeList.featureLayer = None
        pass

    def onPaddockFilterChanged(self, text):
        self.paddockList.filterByName(text)
