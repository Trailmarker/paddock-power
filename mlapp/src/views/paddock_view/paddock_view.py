# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from ..view_base import ViewBase

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_view_base.ui')))


class PaddockView(ViewBase, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(project, parent)

        self.setupUi(self)

        self.paddockList.featureLayer = self.project.paddockLayer
        self.paddockList.featureZoomed.connect(self.project.zoomFeature)

        self.paddockFilterLineEdit.textChanged.connect(
            self.onPaddockFilterChanged)
        self.clearPaddockFilterButton.clicked.connect(
            self.paddockFilterLineEdit.clear)

    def onPaddockFilterChanged(self, text):
        self.paddockList.filterByName(text)
