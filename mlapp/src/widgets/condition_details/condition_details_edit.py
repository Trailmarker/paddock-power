# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'condition_details_edit_base.ui')))


class ConditionDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, condition, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.condition = condition

        self.conditionComboBox.setEnabled(False)

        # if self.condition is not None:
        #     self.nameLineEdit.setText(self.condition.name)

    @pyqtSlot()
    def saveFeature(self):
        """Save the Condition Details."""
        # self.condition.name = self.nameLineEdit.text()
        # self.condition.upsert()
