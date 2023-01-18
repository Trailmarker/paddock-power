# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ..spatial.features.fence import Fence
from ..spatial.features.persisted_feature import Feature
from ..tools.sketch_line_tool import SketchLineTool
from ..widgets.profile_details.profile_details_dialog import ProfileDetailsDialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_widget_base.ui')))


class FenceWidget(QWidget, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.project = project

        self.setupUi(self)

        self.profileDetailsDialog = ProfileDetailsDialog(self.project, self)

        self.fenceList.featureLayer = self.project.fenceLayer
        self.fencePaddockChanges.setProject(self.project)

        self.splitter.setSizes([self.fenceListGroupBox.sizeHint().width(),
                               self.fencePaddockChanges.sizeHint().width()])
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, True)

        self.project.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)

    def sketchFence(self):
        """Sketch and analyse a new Fence."""
        tool = SketchLineTool(self.project)
        tool.sketchFinished.connect(self.onSketchFenceFinished)
        self.project.setTool(tool)

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, feature):
        """Handle a change to the selected Fence."""
        if isinstance(feature, Fence):
            self.profileDetailsDialog.show()

    @pyqtSlot(QgsGeometry)
    def onSketchFenceFinished(self, sketchLine):
        fence = self.project.fenceLayer.makeFeature()
        fence.draftFeature(sketchLine)
        self.project.selectFeature(fence)
