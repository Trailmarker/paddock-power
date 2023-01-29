# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ..tools.sketch_line_tool import SketchLineTool


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'pipeline_widget_base.ui')))


class PipelineWidget(QWidget, FORM_CLASS):

    def __init__(self, workspace, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.workspace = workspace

        self.setupUi(self)

        self.pipelineList.setFeatureLayer(self.workspace.pipelineLayer)

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, True)

    def sketchPipeline(self):
        """Sketch a new Pipeline."""
        tool = SketchLineTool(self.workspace)
        tool.sketchFinished.connect(self.onSketchPipelineFinished)
        self.workspace.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchPipelineFinished(self, sketchLine):
        pipeline = self.workspace.pipelineLayer.makeFeature()
        pipeline.planFeature(sketchLine)
        self.workspace.selectFeature(pipeline)
