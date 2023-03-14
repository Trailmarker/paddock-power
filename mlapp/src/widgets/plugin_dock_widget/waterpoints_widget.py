# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsGeometry

from ...models import WorkspaceMixin
from ..feature_table import SplitFeatureTablesWidget, WaterpointTable
from ..tools import SketchPointTool


class WaterpointsWidget(WorkspaceMixin, SplitFeatureTablesWidget):

    def __init__(self, parent=None):
        """Constructor."""
        WorkspaceMixin.__init__(self)
        SplitFeatureTablesWidget.__init__(self, parent)

        self.addFeatureTable("Waterpoints", WaterpointTable)

    def sketchWaterpoint(self):
        """Sketch a new Waterpoint."""
        tool = SketchPointTool()
        tool.sketchFinished.connect(self.onSketchWaterpointFinished)
        self.workspace.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchWaterpointFinished(self, sketchPoint):
        waterpoint = self.workspace.waterpointLayer.makeFeature()
        waterpoint.draftFeature(sketchPoint)
        self.workspace.selectFeature(waterpoint)
