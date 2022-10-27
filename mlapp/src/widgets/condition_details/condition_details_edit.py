# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ...spatial.schemas.condition_type import ConditionType

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'condition_details_edit_base.ui')))


class ConditionDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, condition, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.condition = condition
        self._conditionType = condition.conditionType

        for conditionType in ConditionType:
            self.conditionTypeComboBox.addItem(conditionType.value, conditionType)

        self.conditionTypeComboBox.setCurrentIndex(
            self.conditionTypeComboBox.findData(self._conditionType))

        self.conditionTypeComboBox.currentIndexChanged.connect(self.setConditionType)

    @pyqtSlot(int)
    def setConditionType(self, index):
        self._conditionType = self.conditionTypeComboBox.itemData(index)

    @pyqtSlot()
    def saveFeature(self):
        """Save the Condition Details."""
        self.condition.upsertCondition(self._conditionType)
