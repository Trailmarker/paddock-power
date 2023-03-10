# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsGeometry

from ..layers.features import Fence
from ..layers.fields import FeatureStatus
from ..models import WorkspaceMixin
from ..utils import qgsDebug
from ..tools.sketch_line_tool import SketchLineTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_widget_base.ui')))


class FenceWidget(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.fence = None
        self.setupUi(self)

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, False)
        self.splitter.setCollapsible(3, True)

        self.affectedPaddocksMiniList.basePaddockLayer = self.basePaddockLayer
        self.resultingPaddocksMiniList.basePaddockLayer = self.basePaddockLayer

        self.fenceLayer.featureSelected.connect(self.changeSelection)
        self.fenceLayer.featureDeselected.connect(self.removeSelection)
        self.refreshUi()

    @property
    def fenceLayer(self):
        return self.workspace.fenceLayer

    @property
    def basePaddockLayer(self):
        return self.workspace.basePaddockLayer

    def sketchFence(self):
        """Sketch and analyse a new Fence."""
        tool = SketchLineTool(self.workspace)
        tool.sketchFinished.connect(self.onSketchFenceFinished)
        self.workspace.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchFenceFinished(self, sketchLine):
        fence = self.workspace.fenceLayer.makeFeature()
        fence.draftFeature(sketchLine)
        # Bump the cache … 
        self.plugin.featureView.fenceTab.fenceTableView.bumpCache()
        self.workspace.selectFeature(fence)

    def changeSelection(self, layerId):
        feature = self.workspace.selectedFeature(layerId)

        if isinstance(feature, Fence):
            self.fence = feature
            self.refreshUi()

    def removeSelection(self):
        self.fence = None
        self.refreshUi()

    def refreshUi(self):
        """Show the Paddock View."""
        if self.fence is None:
            self.affectedPaddocksGroupBox.setVisible(False)
            self.resultingPaddocksGroupBox.setVisible(False)
            self.affectedPaddocksMiniList.clear()
            self.resultingPaddocksMiniList.clear()
        else:
            affectedPaddocks, resultingPaddocks = self.fence.getRelatedPaddocks()

            if self.fence.matchStatus(FeatureStatus.Drafted):
                self.affectedPaddocksGroupBox.setTitle("Crossed Paddocks")
                self.resultingPaddocksGroupBox.setTitle("New Paddocks")
            elif self.fence.matchStatus(FeatureStatus.Planned):
                self.affectedPaddocksGroupBox.setTitle("Superseded Paddocks")
                self.resultingPaddocksGroupBox.setTitle("Planned Paddocks")
            elif self.fence.matchStatus(FeatureStatus.Built):
                self.affectedPaddocksGroupBox.setTitle("Archived Paddocks")
                self.resultingPaddocksGroupBox.setTitle("Built Paddocks")

            # Hide these Paddock group boxes if there's no content
            self.affectedPaddocksGroupBox.setVisible(bool(affectedPaddocks))
            self.resultingPaddocksGroupBox.setVisible(bool(resultingPaddocks))
            self.affectedPaddocksMiniList.setFeatures(affectedPaddocks)
            self.resultingPaddocksMiniList.setFeatures(resultingPaddocks)
