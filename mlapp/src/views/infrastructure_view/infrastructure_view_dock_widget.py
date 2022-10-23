# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtWidgets import QDockWidget

from ...models.glitch import Glitch
from ...models.state import State, connectStateListener
from .sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'infrastructure_view_dock_widget_base.ui')))


class InfrastructureViewDockWidget(QDockWidget, FORM_CLASS):

    closingDockWidget = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.state = State()

        self.setupUi(self)

        # self.sketchInfrastructureLineButton.setIcon(
        #     QIcon(":/plugins/mlapp/images/new-split-paddock.png"))
        # self.selectInfrastructureLineButton.setIcon(
        #     QIcon(":/plugins/mlapp/images/new-split-paddock.png"))

        connectStateListener(self.state, self)

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
    def onSelectedFeatureChanged(self, _):
        self.refreshUi()

    def sketchFence(self):
        """Sketch and analyse a new Fence."""
        project = self.state.getProject()

        if project is None:
            raise Glitch("Please set the current Project before using the Sketch Line tool.")
        else:
            tool = SketchLineTool(project)
            tool.sketchFinished.connect(
                lambda sketchLine: self.onSketchFenceFinished(sketchLine))
            project.setTool(tool)

    @pyqtSlot()
    def onSketchFenceFinished(self, sketchLine):
        project = self.state.getProject()

        fence = project.fenceLayer.makeFeature()
        fence.draftFence(sketchLine)

        # project.setSelectedFeature(fence)

    def sketchPipeline(self):
        """Sketch a new Pipeline."""
        project = self.state.getProject()

        if project is None:
            raise Glitch("Please set the current Project before using the Sketch Line tool.")
        else:
            tool = SketchLineTool(project)
            tool.sketchFinished.connect(self.onSketchPipelineFinished)
            project.setTool(tool)

    @pyqtSlot()
    def onSketchPipelineFinished(self, sketchLine):
        project = self.state.getProject()

        pipeline = project.pipelineLayer.makeFeature()
        pipeline.draftPipeline(sketchLine)
        pipeline.planPipeline()
        project.setSelectedFeature(pipeline)

    def refreshUi(self):
        """Show the Infrastructure Profile."""
        # If we have no current infrastructure profile data, clean up the canvas object
        project = self.state.getProject()

        for button in [self.sketchFenceButton,
                       self.sketchPipelineButton,
                       self.selectFenceButton,
                       self.selectPipelineButton]:
            button.setEnabled(project is not None)

    def closeEvent(self, event):
        self.closingDockWidget.emit()
        event.accept()
