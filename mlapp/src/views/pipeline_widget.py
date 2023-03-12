# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ..models import WorkspaceMixin
from ..tools.sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'pipeline_widget_base.ui')))


class PipelineWidget(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)
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
        pipeline.draftFeature(sketchLine)
        # Bump the cache … 
        # self.plugin.featureView.pipelineTab.pipelineTableView.bumpCache()
        self.workspace.selectFeature(pipeline)
