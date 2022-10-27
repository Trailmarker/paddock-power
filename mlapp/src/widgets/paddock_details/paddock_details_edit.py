# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_details_edit_base.ui')))


class PaddockDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, paddock, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.paddock = paddock

        if self.paddock is not None:
            self.nameLineEdit.setText(self.paddock.name)

    @pyqtSlot()
    def savePaddock(self):
        """Save the Paddock Details."""
        self.paddock.name = self.nameLineEdit.text()
        self.paddock.upsert()
