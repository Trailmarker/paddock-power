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
            self.areaText.setText(f"{self.paddock.featureArea:2f}")
            self.perimeterText.setText(f"{self.paddock.featurePerimeter:2f}")
            self.estimatedCapacityText.setText(f"{self.paddock.estimatedCapacity:g}")
            self.potentialCapacityText.setText(f"{self.paddock.potentialCapacity:g}")
            self.capacityPerAreaText.setText(f"{self.paddock.capacityPerArea:1f}")