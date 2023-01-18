# -*- coding: utf-8 -*-
import os


from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QDialog

from ...spatial.features.feature import Feature

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'profile_details_dialog_base.ui')))


class ProfileDetailsDialog(QDialog, FORM_CLASS):
    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        project.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)

        self.profileDetails.setProject(project)
        self.profileDetails.refreshUi()

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, feature):
        """Change the ProfileDetailsDialog title depending on the new selected Feature."""
        if feature and feature.isInfrastructure:
            self.setWindowTitle(f"Elevation Profile - {feature.title}")
        else:
            self.setWindowTitle(f"Elevation Profile")
