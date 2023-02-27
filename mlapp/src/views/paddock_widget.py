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

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, False)
        self.splitter.setCollapsible(3, True)

        self.currentPaddockLandTypesList.popupLayerSource = self.workspace.paddockLayer
        self.futurePaddockLandTypesList.popupLayerSource = self.workspace.paddockLayer

        self.paddockFilterLineEdit.textChanged.connect(
            self.onPaddockFilterChanged)
        self.clearPaddockFilterButton.clicked.connect(
            self.paddockFilterLineEdit.clear)

    def onPaddockFilterChanged(self, text):
        self.paddockList.filterByName(text)

    def refreshUi(self):
        self.paddockList.clearAndRefreshCache()
        self.currentPaddockLandTypesList.clearAndRefreshCache()
        self.futurePaddockLandTypesList.clearAndRefreshCache()
