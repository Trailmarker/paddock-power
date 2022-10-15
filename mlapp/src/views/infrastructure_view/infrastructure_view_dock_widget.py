# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtWidgets import QDockWidget

from ...models.paddock_power_state import PaddockPowerState, connectPaddockPowerStateListener
from ...spatial.feature.fence import makeFence
from ...spatial.feature.feature_status import FeatureStatus
from ...spatial.feature.pipeline import makePipeline
from ...utils import guiError
from .sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'infrastructure_view_dock_widget_base.ui')))


class InfrastructureViewDockWidget(QDockWidget, FORM_CLASS):

    closingDockWidget = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        # self.sketchInfrastructureLineButton.setIcon(
        #     QIcon(":/plugins/mlapp/images/new-split-paddock.png"))
        # self.selectInfrastructureLineButton.setIcon(
        #     QIcon(":/plugins/mlapp/images/new-split-paddock.png"))

        self.state = PaddockPowerState()
        connectPaddockPowerStateListener(self.state, self)

        self.sketchFenceButton.clicked.connect(
            self.sketchFence)

        self.sketchPipelineButton.clicked.connect(
            self.sketchPipeline)

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
    def onSelectedFenceChanged(self, _):
        self.refreshUi()

    @pyqtSlot()
    def onSelectedPipelineChanged(self, _):
        self.refreshUi()

    def sketchFence(self):
        """Sketch and analyse a new Fence."""
        milestone = self.state.getMilestone()

        if milestone is None:
            guiError(
                "Please set the current Milestone before using the Sketch Line tool.")
        else:
            tool = SketchLineTool(milestone)
            tool.sketchFinished.connect(
                lambda sketchLine: self.onSketchFenceFinished(sketchLine))
            milestone.setTool(tool)

    @pyqtSlot()
    def onSketchFenceFinished(self, sketchLine):
        milestone, project = self.state.getMilestone(), self.state.getProject()

        fence = makeFence()
        fence.setGeometry(sketchLine)
        fence.recalculate(project.elevationLayer)

        draftFence = milestone.draftFence(fence)
        if draftFence is not None:
            milestone.setSelectedFence(draftFence)

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
        pipeline.setStatus(FeatureStatus.Planned)

        milestone.setSelectedPipeline(pipeline)

    def refreshUi(self):
        """Show the Infrastructure Profile."""
        # If we have no current infrastructure profile data, clean up the canvas object
        milestone = self.state.getMilestone()

        for button in [self.sketchFenceButton,
                       self.sketchPipelineButton,
                       self.selectFenceButton,
                       self.selectPipelineButton]:
            button.setEnabled(milestone is not None)

    def closeEvent(self, event):
        self.closingDockWidget.emit()
        event.accept()
