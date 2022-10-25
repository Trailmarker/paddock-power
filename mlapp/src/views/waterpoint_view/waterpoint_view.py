# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsGeometry

from ...tools.sketch_point_tool import SketchPointTool
from ..view_base import ViewBase

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'waterpoint_view_base.ui')))


class WaterpointView(ViewBase, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(project, parent)

        self.setupUi(self)

        self.waterpointList.featureLayer = self.project.waterpointLayer
        self.waterpointList.featureZoomed.connect(self.project.zoomFeature)
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
