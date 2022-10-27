# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsGeometry

from ..view_base import ViewBase
from ...tools.sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'pipeline_view_base.ui')))


class PipelineView(ViewBase, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(project, parent)

        self.setupUi(self)

        self.pipelineList.featureLayer = self.project.pipelineLayer
        self.profileDetails.setProject(self.project)

        self.sketchPipelineButton.clicked.connect(self.sketchPipeline)

    def sketchPipeline(self):
        """Sketch a new Pipeline."""
        tool = SketchLineTool(self.project)
        tool.sketchFinished.connect(self.onSketchPipelineFinished)
        self.project.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchPipelineFinished(self, sketchLine):
        pipeline = self.project.pipelineLayer.makeFeature()
        pipeline.planFeature(sketchLine)
        self.project.selectFeature(pipeline)
