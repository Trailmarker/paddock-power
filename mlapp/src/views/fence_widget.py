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

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.project = project

        self.setupUi(self)

        self.fenceList.featureLayer = self.project.fenceLayer
        self.fencePaddockChanges.setProject(self.project)

        self.splitter.setSizes([self.fenceListGroupBox.sizeHint().width(),
                               self.fencePaddockChanges.sizeHint().width()])
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, True)

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
