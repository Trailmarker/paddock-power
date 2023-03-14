# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ..models import WorkspaceMixin
from ..tools.sketch_point_tool import SketchPointTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'waterpoint_widget_base.ui')))


class WaterpointWidget(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)
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
        # Bump the cache …
        # self.plugin.featureView.waterpointTab.waterpointTable.bumpCache()
        self.workspace.selectFeature(waterpoint)
