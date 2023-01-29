# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ..tools.sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_widget_base.ui')))


class FenceWidget(QWidget, FORM_CLASS):

    def __init__(self, workspace, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.workspace = workspace

        self.setupUi(self)

        self.fenceList.featureLayer = self.workspace.fenceLayer
        self.fencePaddockChanges.setWorkspace(self.workspace)

        self.splitter.setSizes([self.fenceListGroupBox.sizeHint().width(),
                               self.fencePaddockChanges.sizeHint().width()])
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, True)

    def sketchFence(self):
        """Sketch and analyse a new Fence."""
        tool = SketchLineTool(self.workspace)
        tool.sketchFinished.connect(self.onSketchFenceFinished)
        self.workspace.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchFenceFinished(self, sketchLine):
        fence = self.workspace.fenceLayer.makeFeature()
        fence.draftFeature(sketchLine)
        self.workspace.selectFeature(fence)
