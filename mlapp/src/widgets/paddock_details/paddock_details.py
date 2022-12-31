# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsProject

from ...utils import qgsDebug

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_details_base.ui')))


class PaddockDetails(QWidget, FORM_CLASS):

    def __init__(self, paddock, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.paddock = paddock
        self._derivedMetricPaddockLayerId = None
        self.metricPaddock = None

    @property
    def derivedMetricPaddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId) if self._derivedMetricPaddockLayerId else None

    @derivedMetricPaddockLayer.setter
    def derivedMetricPaddockLayer(self, derivedMetricPaddockLayer):
        """Set the FeatureLayer and update the display."""
        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id() if derivedMetricPaddockLayer else None

        if derivedMetricPaddockLayer and self.paddock:
            self.metricPaddock = derivedMetricPaddockLayer.getFeatureByPaddockId(self.paddock.id)

            if self.metricPaddock is not None:
                self.areaText.setValue(self.metricPaddock.featureArea, "{0:.1f}")
                self.perimeterText.setValue(self.metricPaddock.featurePerimeter, "{0:.1f}")
                self.estimatedCapacityText.setValue(self.metricPaddock.estimatedCapacity, "{0:.0f}")
                self.potentialCapacityText.setValue(self.metricPaddock.potentialCapacity, "{0:.0f}")
                self.estimatedCapacityPerAreaText.setValue(self.metricPaddock.estimatedCapacityPerArea, "{0:.1f}")
                # self.potentialCapacityPerAreaText.setValue(self.metricPaddock.potentialCapacityPerArea, "{0:.1f}")
