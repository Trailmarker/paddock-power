# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ...tools.sketch_point_tool import SketchPointTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'waterpoint_widget_base.ui')))


class WaterpointWidget(QWidget, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.project = project

        self.setupUi(self)

        self.waterpointList.featureLayer = self.project.waterpointLayer
        self.sketchWaterpointButton.clicked.connect(self.sketchWaterpoint)

    def sketchWaterpoint(self):
        """Sketch and analyse a new Fence."""
        tool = SketchPointTool(self.project)
        tool.sketchFinished.connect(self.onSketchWaterpointFinished)
        self.project.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchWaterpointFinished(self, sketchPoint):
        waterpoint = self.project.waterpointLayer.makeFeature()
        waterpoint.draftFeature(sketchPoint)
        self.project.selectFeature(waterpoint)
