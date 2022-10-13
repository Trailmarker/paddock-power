# -*- coding: utf-8 -*-
import os
from mlapp.src.models.paddock_power_error import PaddockPowerError

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDockWidget, QSizePolicy


from ...layer.calculator import Calculator
from ...layer.fence import Fence, asFence, makeFence
from ...layer.paddock_power_feature_status import PaddockPowerFeatureStatus
from ...layer.pipeline import Pipeline, asPipeline, makePipeline
from ...models.paddock_power_state import PaddockPowerState, connectPaddockPowerStateListener
from ...utils import guiError, qgsDebug
from ...widgets.infrastructure_profile.profile_canvas import ProfileCanvas
from .sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'infrastructure_view_dock_widget_base.ui')))


class InfrastructureViewDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(QDockWidget, self).__init__(parent)

        self.setupUi(self)

        self.selectedInfrastructure = None
        self.profileCanvas = None

        self.sketchInfrastructureLineButton.setIcon(
            QIcon(":/plugins/mlapp/images/new-split-paddock.png"))
        self.selectInfrastructureLineButton.setIcon(
            QIcon(":/plugins/mlapp/images/new-split-paddock.png"))

        self.sketchInfrastructureLineButton.clicked.connect(
            self.sketchFence)

        self.state = PaddockPowerState()
        connectPaddockPowerStateListener(self.state, self)

        self.refreshUi()

    def showEvent(self, event):
        self.state.detectProject()

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
        self.setSelectedInfrastructure(asFence(fence))

    @pyqtSlot()
    def onSelectedPipelineChanged(self, pipeline):
        """Handle a change to the selected Pipeline."""
        self.setSelectedInfrastructure(asPipeline(pipeline))

    def setSelectedInfrastructure(self, infrastructure):
        """Set the selected Infrastructure."""
        if not isinstance(infrastructure, Fence) and not isinstance(infrastructure, Pipeline):
            raise PaddockPowerError("InfrastructureViewDockWidget.setSelectedInfrastructure: infrastructure is not a Fence or Pipeline")
        self.selectedInfrastructure = infrastructure

        self.refreshUi()

    def sketchFence(self):
        """Sketch and analyse a new Fence."""
        milestone = self.state.getMilestone()

        if milestone is None:
            guiError(
                "Please set the current Milestone before using the Sketch Line tool.")
        else:
            tool = SketchLineTool(milestone)
            tool.sketchFinished.connect(lambda sketchLine: self.onSketchFenceFinished(sketchLine))
            milestone.setTool(tool)

    @pyqtSlot()
    def onSketchFenceFinished(self, sketchLine):
        milestone, project = self.state.getMilestone(), self.state.getProject()

        fence = makeFence()
        fence.setGeometry(sketchLine)
        fence.recalculate(project.elevationLayer)
        fence.setStatus(PaddockPowerFeatureStatus.Planned)

        if not isinstance(fence, Fence):
            raise PaddockPowerError("InfrastructureViewDockWidget.onSketchFenceFinished: fence is not a Fence")
        
        milestone.setSelectedFence(fence)

    def sketchPipeline(self):
        """Sketch a new Pipeline."""
        milestone = self.state.getMilestone()

        if milestone is None:
            guiError(
                "Please set the current Milestone before using the Sketch Line tool.")
        else:
            tool = SketchLineTool(milestone)
            tool.sketchFinished.connect(self.onSketchPipelineFinished)
            milestone.setTool(tool)

    @pyqtSlot()
    def onSketchPipelineFinished(self, sketchLine):
        milestone, project = self.state.getMilestone(), self.state.getProject()
        
        pipeline = makePipeline()
        pipeline.setGeometry(sketchLine)
        pipeline.recalculate(project.elevationLayer)
        pipeline.setStatus(PaddockPowerFeatureStatus.Planned)
        
        milestone.setSelectedPipeline(pipeline)

    def refreshUi(self):
        """Show the Infrastructure Profile."""
        # If we have no current infrastructure profile data, clean up the canvas object
        if self.selectedInfrastructure is None:
            if self.profileCanvas is not None:
                self.gridLayout.removeWidget(self.profileCanvas)
                del self.profileCanvas
                self.profileCanvas = None

        if self.selectedInfrastructure is not None:
            milestone, project = self.state.getMilestone(), self.state.getProject()

            if milestone is None:
                guiError(
                    "Please set the current Milestone before using the Sketch Infrastructure Line tool.")
                self.selectedInfrastructure = None
                self.refreshUi()

            profile = self.selectedInfrastructure.getProfile()

            if profile is None:
                profile = Calculator.calculateProfile(
                    self.selectedInfrastructure.geometry(), project.elevationLayer)

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

            self.profileCanvas = ProfileCanvas(profile)
            self.profileCanvas.setSizePolicy(QSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))

            self.profileCanvas.setMaximumHeight(250)
            self.gridLayout.addWidget(
                self.profileCanvas, 4, 0, 1, 4)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
