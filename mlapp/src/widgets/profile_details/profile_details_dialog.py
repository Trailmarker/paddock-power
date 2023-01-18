# -*- coding: utf-8 -*-
import os


from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QDialog

from ...spatial.features.feature import Feature

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'profile_details_dialog_base.ui')))


class ProfileDetailsDialog(QDialog, FORM_CLASS):
    def __init__(self, feature, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.feature = feature
        self.setupUi(self)

        self.setWindowTitle(f"Elevation Profile - {self.feature.title}")
        self.profileDetails.setFeature(self.feature)
