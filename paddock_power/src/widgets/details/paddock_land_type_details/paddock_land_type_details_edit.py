# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ....layers.features import Edits
from ....layers.fields import ConditionType
from ...delegates import FieldDomainDelegate


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_land_type_details_edit_base.ui')))


class PaddockLandTypeDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, paddockLandType, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.paddockLandType = paddockLandType
        self._conditionType = paddockLandType.CONDITION_TYPE

        self.conditionTypeComboBox.setItemDelegate(FieldDomainDelegate(ConditionType, self))
        for conditionType in ConditionType:
            self.conditionTypeComboBox.addItem(conditionType.value, conditionType)

        self.conditionTypeComboBox.setCurrentIndex(
            self.conditionTypeComboBox.findData(self._conditionType))

        self.conditionTypeComboBox.currentIndexChanged.connect(self.setConditionType)

    @pyqtSlot(int)
    def setConditionType(self, index):
        self._conditionType = self.conditionTypeComboBox.itemData(index)

    def saveFeature(self):
        """Save the Paddock Land Type details, updating the Condition Type."""
        self.paddockLandType.CONDITION_TYPE = self._conditionType
        return Edits.upsert(self.paddockLandType.landTypeCondition)
