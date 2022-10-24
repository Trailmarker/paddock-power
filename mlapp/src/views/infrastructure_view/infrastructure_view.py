# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot

from ...spatial.features.feature import Feature
from ..view_base import ViewBase
from .sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'infrastructure_view_base.ui')))


class InfrastructureView(ViewBase, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(project, parent)

        self.setupUi(self)

        self.fenceList.featureLayer = self.project.fenceLayer
        self.fenceList.featureZoomed.connect(self.project.zoomFeature)
        self.fencePaddockChanges.setProject(self.project)
        self.profileDetails.setProject(self.project)

        # self.sketchInfrastructureLineButton.setIcon(
        #     QIcon(":/plugins/mlapp/images/new-split-paddock.png"))
        # self.selectInfrastructureLineButton.setIcon(
        #     QIcon(":/plugins/mlapp/images/new-split-paddock.png"))

        self.sketchFenceButton.clicked.connect(
            self.sketchFence)

        self.sketchPipelineButton.clicked.connect(
            self.sketchPipeline)

    def sketchFence(self):
        """Sketch and analyse a new Fence."""
        tool = SketchLineTool(self.project)
        tool.sketchFinished.connect(
            lambda sketchLine: self.onSketchFenceFinished(sketchLine))
        self.project.setTool(tool)

    @pyqtSlot()
    def onSketchFenceFinished(self, sketchLine):
        fence = self.project.fenceLayer.makeFeature()
        fence.draftFence(sketchLine)
        self.project.selectFeature(fence)

    def sketchPipeline(self):
        """Sketch a new Pipeline."""
        tool = SketchLineTool(self.project)
        tool.sketchFinished.connect(self.onSketchPipelineFinished)
        self.project.setTool(tool)

    @pyqtSlot()
    def onSketchPipelineFinished(self, sketchLine):
        pipeline = self.project.pipelineLayer.makeFeature()
        pipeline.draftPipeline(sketchLine)
        pipeline.planPipeline()
        self.project.selectFeature(pipeline)
