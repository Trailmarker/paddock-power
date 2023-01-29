# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QSizePolicy, QWidget

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

        self.feature = None
        self.workspace = None
        self.profileCanvas = None

        self.refreshUi()

    def setFeature(self, feature):
        """Set the Feature."""
        if feature and feature.isInfrastructure:
            self.feature = feature
        else:
            self.feature = None

        self.refreshUi()

    def setWorkspace(self, workspace):
        """Set the Workspace."""
        self.workspace = workspace
        self.workspace.selectedFeaturesChanged.connect(self.onSelectedFeaturesChanged)
        self.refreshUi()

    def refreshUi(self):
        """Refresh the UI."""
        # If we have no current selected infrastructure, hide stuff
        for label in [self.elevationRangeLabel, self.elevationRangeText,
                      self.infrastructureLengthLabel, self.infrastructureLengthText]:
            label.setVisible(self.feature is not None)

        if self.feature is None:
            self.cleanupProfileCanvas()
            return

        if self.feature is not None:

            if self.feature.profile() is None:
                self.feature.recalculate()

            profile = self.feature.profile()

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

            self.refreshProfileCanvas()
            self.update()

    def cleanupProfileCanvas(self):
        if self.profileCanvas is not None:
            self.canvasLayout.removeWidget(self.profileCanvas)
            del self.profileCanvas
            self.profileCanvas = None

    def refreshProfileCanvas(self):
        self.cleanupProfileCanvas()
        self.profileCanvas = ProfileCanvas(self.feature.profile(), layout=self.canvasLayout)
        self.profileCanvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvasLayout.addWidget(self.profileCanvas)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.refreshUi()

    @pyqtSlot(type, list)
    def onSelectedFeaturesChanged(self, featureLayerType, features):
        """Handle a change to the selected Fence."""
        feature = features[0] if features else None
        self.setFeature(feature)
