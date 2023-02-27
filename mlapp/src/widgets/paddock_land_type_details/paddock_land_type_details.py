# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_land_type_details_base.ui')))


class PaddockLandTypeDetails(QWidget, FORM_CLASS):

    def __init__(self, paddockLandType, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)
        self.paddockLandType = paddockLandType

    def refreshUi(self):
        if self.paddockLandType is not None:
            self.landTypeNameText.setValue(self.paddockLandType.LAND_TYPE_NAME, "{0}")
            self.conditionTypeText.setValue(self.paddockLandType.CONDITION_TYPE.value, "{0}")
            self.areaText.setValue(self.paddockLandType.AREA, "{0:.2f}")
            self.wateredAreaText.setValue(self.paddockLandType.WATERED_AREA, "{0:.2f}")
            self.estimatedCapacityText.setValue(self.paddockLandType.ESTIMATED_CAPACITY, "{0:.0f}")
            self.potentialCapacityText.setValue(self.paddockLandType.POTENTIAL_CAPACITY, "{0:.0f}")
            self.estimatedCapacityPerAreaText.setValue(self.paddockLandType.ESTIMATED_CAPACITY_PER_AREA, "{0:.1f}")
            # self.potentialCapacityPerAreaText.setValue(self.paddockLandType.potentialCapacityPerArea, "{0:.1f}")
