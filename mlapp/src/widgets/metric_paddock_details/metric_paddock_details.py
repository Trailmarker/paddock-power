# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'metric_paddock_details_base.ui')))


class MetricPaddockDetails(QWidget, FORM_CLASS):

    def __init__(self, metricPaddock, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.metricPaddock = metricPaddock

        if self.metricPaddock is not None:
            self.areaText.setValue(self.metricPaddock.AREA, "{0:.2f}")
            self.wateredAreaText.setValue(self.metricPaddock.WATERED_AREA, "{0:.2f}")
            self.perimeterText.setValue(self.metricPaddock.PERIMETER, "{0:.1f}")
            self.estimatedCapacityText.setValue(self.metricPaddock.ESTIMATED_CAPACITY, "{0:.0f}")
            self.potentialCapacityText.setValue(self.metricPaddock.POTENTIAL_CAPACITY, "{0:.0f}")
            self.estimatedCapacityPerAreaText.setValue(self.metricPaddock.ESTIMATED_CAPACITY_PER_AREA, "{0:.1f}")
            self.wateredAreaText.setValue(self.metricPaddock.WATERED_AREA, "{0:.2f}")
            # self.potentialCapacityPerAreaText.setValue(self.metricPaddock.potentialCapacityPerArea, "{0:.1f}")
