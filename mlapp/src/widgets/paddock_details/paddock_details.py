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
            self.areaText.setValue(self.paddock.AREA, "{0:.2f}")
            self.wateredAreaText.setValue(self.paddock.WATERED_AREA, "{0:.2f}")
            self.perimeterText.setValue(self.paddock.PERIMETER, "{0:.1f}")
            self.estimatedCapacityText.setValue(self.paddock.ESTIMATED_CAPACITY, "{0:.0f}")
            self.potentialCapacityText.setValue(self.paddock.POTENTIAL_CAPACITY, "{0:.0f}")
            self.estimatedCapacityPerAreaText.setValue(self.paddock.ESTIMATED_CAPACITY_PER_AREA, "{0:.1f}")
            self.wateredAreaText.setValue(self.paddock.WATERED_AREA, "{0:.2f}")
            # self.potentialCapacityPerAreaText.setValue(self.paddock.potentialCapacityPerArea, "{0:.1f}")
