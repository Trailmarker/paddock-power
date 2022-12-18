# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ...spatial.features.persisted_feature import Feature
from .profile_canvas import ProfileCanvas

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'profile_details_base.ui')))


class ProfileDetails(QWidget, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.elevationRangeLabel.setProperty("class", "form-left")
        self.elevationRangeText.setProperty("class", "form-right")
        self.infrastructureLengthLabel.setProperty("class", "form-left")
        self.infrastructureLengthText.setProperty("class", "form-right")

        self.project = None
        self.selectedInfrastructure = None
        self.profileCanvas = None

        self.refreshUi()

    def setProject(self, project):
        """Set the Project."""
        self.project = project
        self.project.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)
        self.refreshUi()

    def refreshUi(self):
        """Refresh the UI."""
        # If we have no current selected infrastructure, hide stuff
        for label in [self.elevationRangeLabel, self.elevationRangeText,
                      self.infrastructureLengthLabel, self.infrastructureLengthText]:
            label.setVisible(self.selectedInfrastructure is not None)

        if self.project is None or self.selectedInfrastructure is None:
            self.cleanupProfileCanvas()
            return

        if self.selectedInfrastructure is not None:
            if self.project is None:
                self.selectedInfrastructure = None
                self.refreshUi()
                return

            if self.selectedInfrastructure.profile() is None:
                self.selectedInfrastructure.recalculate()

            profile = self.selectedInfrastructure.profile()

            useMetres = (profile.maximumDistance < 1000)

            maximumDistance = profile.maximumDistance if useMetres else profile.maximumDistance / 1000
            self.elevationRangeText.setText(
                f"{profile.minimumElevation:,.0f} – {profile.maximumElevation:,.0f} (mean {profile.meanElevation})")

            if useMetres:
                self.infrastructureLengthLabel.setText(
                    "Minimum estimated length (m)")
                self.infrastructureLengthText.setText(
                    f"{maximumDistance:,.0f}")
            else:
                self.infrastructureLengthLabel.setText(
                    "Minimum estimated length (km)")
                self.infrastructureLengthText.setText(
                    f"{maximumDistance:,.2f}")

            self.refreshProfileCanvas(profile)

    def cleanupProfileCanvas(self):
        if self.profileCanvas is not None:
            self.canvasLayout.removeWidget(self.profileCanvas)
            del self.profileCanvas
            self.profileCanvas = None

    def refreshProfileCanvas(self, profile):
        self.cleanupProfileCanvas()
        self.profileCanvas = ProfileCanvas(profile)
        self.canvasLayout.addWidget(self.profileCanvas)

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, feature):
        """Handle a change to the selected Fence."""
        if feature.isInfrastructure:
            self.selectedInfrastructure = feature
            self.refreshUi()
