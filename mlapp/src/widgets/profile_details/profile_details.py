# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget, QLabel

from ...spatial.features.fence import Fence
from ...spatial.features.pipeline import Pipeline
from ...models.glitch import Glitch
from ...models.state import State, connectStateListener
from .profile_canvas import ProfileCanvas

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'profile_details_base.ui')))


class ProfileDetails(QWidget, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.selectedInfrastructure = None
        self.profileCanvas = None

        self.state = State()
        connectStateListener(self.state, self)

        self.refreshUi()

    def refreshUi(self):
        """Refresh the UI."""
        # If we have no current selected infrastructure, hide stuff
        for label in [self.elevationRangeLabel, self.elevationRangeText, self.infrastructureLengthLabel, self.infrastructureLengthText]:
            label.setVisible(self.selectedInfrastructure is not None)
        
        if self.selectedInfrastructure is None:
            self.cleanupProfileCanvas()
            return

        if self.selectedInfrastructure is not None:
            milestone = self.state.getMilestone()

            if milestone is None:
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
            self.setVisible(True)

    def cleanupProfileCanvas(self):
        if self.profileCanvas is not None:
            self.canvasLayout.removeWidget(self.profileCanvas)
            del self.profileCanvas
            self.profileCanvas = None

    def refreshProfileCanvas(self, profile):
        self.cleanupProfileCanvas()
        self.profileCanvas = ProfileCanvas(profile)
        self.canvasLayout.addWidget(self.profileCanvas)

    @pyqtSlot()
    def onProjectChanged(self, project):
        """Handle a change in the current Paddock Power project."""
        self.refreshUi()

    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        """Handle a change in the current Paddock Power milestone."""
        self.refreshUi()

    @pyqtSlot()
    def onSelectedFenceChanged(self, fence):
        """Handle a change to the selected Fence."""
        self.setSelectedInfrastructure(fence)

    @pyqtSlot()
    def onSelectedPipelineChanged(self, pipeline):
        """Handle a change to the selected Pipeline."""
        self.setSelectedInfrastructure(pipeline)

    def setSelectedInfrastructure(self, infrastructure):
        """Set the selected Infrastructure."""
        if not isinstance(infrastructure, Fence) and not isinstance(infrastructure, Pipeline):
            raise Glitch(
                "InfrastructureViewDockWidget.setSelectedInfrastructure: infrastructure is not a Fence or Pipeline")
        self.selectedInfrastructure = infrastructure

        self.refreshUi()