# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_land_system_details_base.ui')))


class PaddockLandSystemDetails(QWidget, FORM_CLASS):

    def __init__(self, paddockLandSystem, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.paddockLandSystem = paddockLandSystem
        if self.paddockLandSystem is not None:
            self.landSystemNameText.setValue(self.paddockLandSystem.landSystemName, "{0}")
            self.conditionTypeText.setValue(self.paddockLandSystem.conditionType.value, "{0}")
            self.areaText.setValue(self.paddockLandSystem.featureArea, "{0:.2f}")
            self.estimatedCapacityText.setValue(self.paddockLandSystem.estimatedCapacity, "{0:.1f}")
            self.potentialCapacityText.setValue(self.paddockLandSystem.potentialCapacity, "{0:.1f}")
            self.estimatedCapacityPerAreaText.setValue(self.paddockLandSystem.estimatedCapacityPerArea, "{0:.1f}")
            self.potentialCapacityPerAreaText.setValue(self.paddockLandSystem.potentialCapacityPerArea, "{0:.1f}")
