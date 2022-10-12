# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDockWidget, QSizePolicy


from ...models.paddock_power_state import PaddockPowerState, connectPaddockPowerStateListener
from ...utils import guiError
from ...widgets.infrastructure_profile.infrastructure_profile_canvas import InfrastructureProfileCanvas
from ...widgets.infrastructure_profile.infrastructure_profile_tool import InfrastructureProfileTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'infrastructure_view_dock_widget_base.ui')))


class InfrastructureViewDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    infrastructureProfile = None
    infrastructureProfileCanvas = None

    def __init__(self, parent=None):
        """Constructor."""
        super(QDockWidget, self).__init__(parent)

        self.setupUi(self)

        self.sketchInfrastructureLineButton.setIcon(
            QIcon(":/plugins/mlapp/images/new-split-paddock.png"))
        self.selectInfrastructureLineButton.setIcon(
            QIcon(":/plugins/mlapp/images/new-split-paddock.png"))

        self.sketchInfrastructureLineButton.clicked.connect(
            self.sketchInfrastructureLine)

        self.state = PaddockPowerState()
        connectPaddockPowerStateListener(self.state, self)

        self.refreshUi()

    @pyqtSlot()
    def onProjectChanged(self, project):
        """Handle a change in the current Paddock Power project."""
        self.refreshUi()

    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        """Handle a change in the current Paddock Power milestone."""
        self.refreshUi()

    @pyqtSlot()
    def onMilestonesUpdated(self, milestones):
        """Handle a change to the current collection of Paddock Power milestones."""
        pass

    def showEvent(self, event):
        self.state.detectProject()

    def sketchInfrastructureLine(self):
        """Set InfrastructureProfileTool as a custom map tool."""
        milestone = self.state.getMilestone()

        if milestone is None:
            guiError(
                "Please set the current Milestone before using the Sketch Infrastructure Line tool.")
        else:
            project = self.state.getProject()
            tool = InfrastructureProfileTool(milestone, project)
            tool.infrastructureProfileUpdated.connect(
                self.setInfrastructureProfile)
            milestone.setTool(tool)

    def setInfrastructureProfile(self, infrastructureProfle):
        """Set the infrastructure profile."""

        # qgsDebug("Fenceline profile is being updated in dock widget …")
        self.infrastructureProfile = infrastructureProfle
        self.refreshUi()

    def refreshUi(self):
        """Show the Infrastructure Profile."""
        # If we have no current infrastructure profile data, clean up the canvas object
        if self.infrastructureProfile is None:
            if self.infrastructureProfileCanvas is not None:
                self.gridLayout.removeWidget(self.infrastructureProfileCanvas)
                del self.infrastructureProfileCanvas
                self.infrastructureProfileCanvas = None
            self.gridLayout.addWidget(self.placeholderLabel, 4, 0, 1, 4)

        if self.infrastructureProfile is not None:
            useMetres = (self.infrastructureProfile.maximumDistance < 1000)

            maximumDistance = self.infrastructureProfile.maximumDistance if useMetres else self.infrastructureProfile.maximumDistance / 1000
            self.elevationRangeText.setText(
                f"{self.infrastructureProfile.minimumElevation:,.0f} – {self.infrastructureProfile.maximumElevation:,.0f}m (mean {self.infrastructureProfile.meanElevation})")

            if useMetres:
                self.infrastructureLengthText.setText(
                    f"{maximumDistance:,.0f}m")
            else:
                self.infrastructureLengthText.setText(
                    f"{maximumDistance:,.2f}km")

            self.infrastructureProfileCanvas = InfrastructureProfileCanvas(
                self.infrastructureProfile)
            self.infrastructureProfileCanvas.setSizePolicy(QSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))

            self.infrastructureProfileCanvas.setMaximumHeight(250)
            self.gridLayout.removeWidget(self.placeholderLabel)
            self.gridLayout.addWidget(
                self.infrastructureProfileCanvas, 4, 0, 1, 4)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
