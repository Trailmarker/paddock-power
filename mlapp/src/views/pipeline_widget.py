# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ..spatial.features.persisted_feature import Feature
from ..spatial.features.pipeline import Pipeline
from ..tools.sketch_line_tool import SketchLineTool
from ..widgets.profile_details.profile_details_dialog import ProfileDetailsDialog


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'pipeline_widget_base.ui')))


class PipelineWidget(QWidget, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.project = project

        self.setupUi(self)

        # self.profileDetailsDialog = ProfileDetailsDialog(self.project, self)

        self.pipelineList.featureLayer = self.project.pipelineLayer

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, True)

        # self.project.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)

    def sketchPipeline(self):
        """Sketch a new Pipeline."""
        tool = SketchLineTool(self.project)
        tool.sketchFinished.connect(self.onSketchPipelineFinished)
        self.project.setTool(tool)

    # @pyqtSlot(Feature)
    # def onSelectedFeatureChanged(self, feature):
    #     """Handle a change to the selected Pipeline."""
    #     # if isinstance(feature, Pipeline):
    #     #     self.profileDetailsDialog.show()
    #     pass

    @pyqtSlot(QgsGeometry)
    def onSketchPipelineFinished(self, sketchLine):
        pipeline = self.project.pipelineLayer.makeFeature()
        pipeline.planFeature(sketchLine)
        self.project.selectFeature(pipeline)
