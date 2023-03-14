# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsGeometry

from ...models import WorkspaceMixin
from ..feature_table import PipelineTable, SplitFeatureTablesWidget
from ..tools import SketchLineTool


class PipelinesWidget(WorkspaceMixin, SplitFeatureTablesWidget):
    """A widget that shows all Pipelines associated with a Property, and allows
       new Pipelines to be sketched, planned and built, with elevation profile
       visualisation."""

    def __init__(self, parent=None):
        """Constructor."""
        WorkspaceMixin.__init__(self)
        SplitFeatureTablesWidget.__init__(self, parent)

        self.addFeatureTable("Pipelines", PipelineTable)

    def sketchPipeline(self):
        """Sketch a new Pipeline."""
        tool = SketchLineTool()
        tool.sketchFinished.connect(self.onSketchPipelineFinished)
        self.workspace.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchPipelineFinished(self, sketchLine):
        pipeline = self.workspace.pipelineLayer.makeFeature()
        pipeline.draftFeature(sketchLine)
        self.workspace.selectFeature(pipeline)
