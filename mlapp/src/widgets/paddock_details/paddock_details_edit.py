# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ...models.paddock_power_state import PaddockPowerState

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_details_edit_base.ui')))


class PaddockDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, paddock, parent=None):
        """Constructor."""
        super(QWidget, self).__init__(parent)

        self.setupUi(self)

        self.state = PaddockPowerState()
        self.paddock = paddock

        if self.paddock is not None:
            self.nameLineEdit.setText(self.paddock.featureName())
            self.conditionComboBox.setEnabled(False)
            self.conditionComboBox.addItem("Not yet implemented")

    @pyqtSlot()
    def savePaddock(self):
        """Save the Paddock Details."""
        milestone = self.state.getMilestone()
        if milestone is not None:
            self.paddock.setFeatureName(self.nameLineEdit.text())
            milestone.paddockLayer.instantCommitFeature(self.paddock)
