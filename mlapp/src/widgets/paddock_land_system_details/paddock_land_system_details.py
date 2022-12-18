# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_land_system_details_base.ui')))


class PaddockLandSystemDetails(QWidget, FORM_CLASS):

    def __init__(self, condition, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.condition = condition
        if self.condition is not None:
            self.landSystemNameText.setValue(self.condition.landSystemName, "{0}")
            self.conditionTypeText.setValue(self.condition.conditionType.value, "{0}")
            self.areaText.setValue(self.condition.featureArea, "{0:2f}")
            self.estimatedCapacityText.setValue(self.condition.estimatedCapacity, "{0:g}")
            self.potentialCapacityText.setValue(self.condition.potentialCapacity, "{0:g}")
            self.estimatedCapacityPerAreaText.setValue(self.condition.estimatedCapacityPerArea, "{0:1f}")
            self.potentialCapacityPerAreaText.setValue(self.condition.potentialCapacityPerArea, "{0:1f}")
