# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_details_base.ui')))


class PaddockDetails(QWidget, FORM_CLASS):

    def __init__(self, paddock, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.paddock = paddock
        if self.paddock is not None:
            self.areaText.setValue(self.paddock.featureArea, "{0:.2f}")
            self.perimeterText.setValue(self.paddock.featurePerimeter, "{0:.2f}")
            self.estimatedCapacityText.setValue(self.paddock.estimatedCapacity, "{0:.1f}")
            self.potentialCapacityText.setValue(self.paddock.potentialCapacity, "{0:.1f}")
            self.estimatedCapacityPerAreaText.setValue(self.paddock.estimatedCapacityPerArea, "{0:.1f}")
            self.potentialCapacityPerAreaText.setValue(self.paddock.potentialCapacityPerArea, "{0:.1f}")

