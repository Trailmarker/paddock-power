# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'condition_details_base.ui')))


class ConditionDetails(QWidget, FORM_CLASS):

    def __init__(self, condition, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.condition = condition
        if self.condition is not None:
            self.landSystemNameText.setText(f"{self.condition.landSystemName}")
            self.conditionTypeText.setText(f"{self.condition.conditionType.value}")
            self.areaText.setText(f"{self.condition.featureArea:2f}")
            self.estimatedCapacityText.setText(f"{self.condition.estimatedCapacity:g}")
            self.potentialCapacityText.setText(f"{self.condition.potentialCapacity:g}")
            self.capacityPerAreaText.setText(f"{self.condition.capacityPerArea:1f}")