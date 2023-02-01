# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ..models import WorkspaceMixin

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

        self.currentPaddockLandTypesList.popupLayerSource = self.workspace.derivedMetricPaddockLayer
        self.futurePaddockLandTypesList.popupLayerSource = self.workspace.derivedMetricPaddockLayer

        self.paddockFilterLineEdit.textChanged.connect(
            self.onPaddockFilterChanged)
        self.clearPaddockFilterButton.clicked.connect(
            self.paddockFilterLineEdit.clear)
        

    def onPaddockFilterChanged(self, text):
        self.paddockList.filterByName(text)
        
    def refreshUi(self):
        self.paddockList.refreshUi()
        self.currentPaddockLandTypesList.refreshUi()
        self.futurePaddockLandTypesList.refreshUi()
