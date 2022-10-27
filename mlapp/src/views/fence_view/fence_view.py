# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsGeometry

from ...tools.sketch_line_tool import SketchLineTool
from ..view_base import ViewBase

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_view_base.ui')))


class FenceView(ViewBase, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(project, parent)

        self.setupUi(self)

        self.fenceList.featureLayer = self.project.fenceLayer
        self.fencePaddockChanges.setProject(self.project)
        self.profileDetails.setProject(self.project)

        self.sketchFenceButton.clicked.connect(self.sketchFence)

    def sketchFence(self):
        """Sketch and analyse a new Fence."""
        tool = SketchLineTool(self.project)
        tool.sketchFinished.connect(self.onSketchFenceFinished)
        self.project.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchFenceFinished(self, sketchLine):
        fence = self.project.fenceLayer.makeFeature()
        fence.draftFeature(sketchLine)
        self.project.selectFeature(fence)
