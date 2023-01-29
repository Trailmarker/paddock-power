# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsProject


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'metric_paddock_details_edit_base.ui')))


class MetricPaddockDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, metricPaddock, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.metricPaddock = metricPaddock
        self._paddockLayerId = None
        self.paddock = None

    @property
    def paddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._paddockLayerId) if self._paddockLayerId else None

    @paddockLayer.setter
    def paddockLayer(self, paddockLayer):
        """Set the FeatureLayer and update the display."""
        self._paddockLayerId = paddockLayer.id() if paddockLayer else None

        if paddockLayer and self.paddock:
            self.paddock = paddockLayer.getFeature(self.metricPaddock.FID)
            self.nameLineEdit.setText(self.paddock.NAME)

    @pyqtSlot()
    def saveFeature(self):
        """Save the Paddock Details."""
        self.paddock.NAME = self.nameLineEdit.text()
