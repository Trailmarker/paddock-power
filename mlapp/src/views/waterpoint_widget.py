# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ..tools.sketch_point_tool import SketchPointTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'waterpoint_widget_base.ui')))


class WaterpointWidget(QWidget, FORM_CLASS):

    def __init__(self, workspace, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.workspace = workspace

        self.setupUi(self)

        self.waterpointList.setFeatureLayer(self.workspace.waterpointLayer)

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, True)

    def sketchWaterpoint(self):
        """Sketch and analyse a new Fence."""
        tool = SketchPointTool(self.workspace)
        tool.sketchFinished.connect(self.onSketchWaterpointFinished)
        self.workspace.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchWaterpointFinished(self, sketchPoint):
        waterpoint = self.workspace.waterpointLayer.makeFeature()
        waterpoint.draftFeature(sketchPoint)
        self.workspace.selectFeature(waterpoint)
