# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ...spatial.features.persisted_feature import PersistedFeature
from ...spatial.features.pipeline import Pipeline
from ...tools.sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'pipeline_widget_base.ui')))


class PipelineWidget(QWidget, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.project = project

        self.setupUi(self)

        self.pipelineList.featureLayer = self.project.pipelineLayer
        self.profileDetails.setProject(self.project)

        self.profileGroupBox.hide()

        # self.splitter.setSizes([self.pipelineListGroupBox.sizeHint().width(), 0])
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, True)

        self.project.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)

    def sketchPipeline(self):
        """Sketch a new Pipeline."""
        tool = SketchLineTool(self.project)
        tool.sketchFinished.connect(self.onSketchPipelineFinished)
        self.project.setTool(tool)

    @pyqtSlot(PersistedFeature)
    def onSelectedFeatureChanged(self, feature):
        """Handle a change to the selected Fence."""
        if isinstance(feature, Pipeline):
            self.profileGroupBox.show()
            self.splitter.setSizes([self.pipelineList.sizeHint().width(), self.profileGroupBox.sizeHint().width()])
        else:
            self.profileGroupBox.hide()

    @pyqtSlot(QgsGeometry)
    def onSketchPipelineFinished(self, sketchLine):
        pipeline = self.project.pipelineLayer.makeFeature()
        pipeline.planFeature(sketchLine)
        self.project.selectFeature(pipeline)
