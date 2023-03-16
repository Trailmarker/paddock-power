# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsGeometry

from ...layers.features import Fence
from ...layers.fields import FeatureStatus
from ...models import WorkspaceMixin
from ..feature_table import BasePaddockTable, FenceTable, SplitFeatureTablesWidget
from ..tools import SketchLineTool


class FencesWidget(WorkspaceMixin, SplitFeatureTablesWidget):
    """A widget that shows three adjacent feature tables: Fences, Affected Paddocks and Resulting Paddocks.
       Selecting Fences shows which Paddocks will be "affected" (split or enclosed by) planned and
       built Fences, and which Paddocks will "result" (be newly enclosed or derived)."""

    def __init__(self, parent=None):
        """Constructor."""
        WorkspaceMixin.__init__(self)
        SplitFeatureTablesWidget.__init__(self, parent)

        self.fence = None

        self.addFeatureTable("Fences", FenceTable)
        self.addFeatureTable("Affected Paddocks", BasePaddockTable, visible=False)
        self.addFeatureTable("Resulting Paddocks", BasePaddockTable, visible=False)

        self.fenceLayer.featureSelected.connect(self.selectFence)
        self.fenceLayer.featureDeselected.connect(self.clearSelectedFence)

    @property
    def fenceLayer(self):
        return self.workspace.fenceLayer

    @property
    def basePaddockLayer(self):
        return self.workspace.basePaddockLayer

    def sketchFence(self):
        """Sketch a new Fence."""
        tool = SketchLineTool()
        tool.sketchFinished.connect(self.onSketchFenceFinished)
        self.workspace.setTool(tool)

    @pyqtSlot(QgsGeometry)
    def onSketchFenceFinished(self, sketchLine):
        fence = self.workspace.fanceLayer.makeFeature()
        fence.draftFeature(sketchLine)
        self.workspace.selectFeature(fence)

    def selectFence(self, _):
        selectedFids = self.fenceLayer.selectedFeatureIds()

        if len(selectedFids) == 1:
            feature = self.fenceLayer.getFeature(selectedFids[0])
            if isinstance(feature, Fence):
                self.fence = feature
                self.relayout()

    def clearSelectedFence(self):
        self.fence = None
        self.relayout()

    _PADDOCK_TABLE_TITLES = {
        FeatureStatus.Drafted: ["Crossed Paddocks", "New Paddocks"],
        FeatureStatus.Planned: ["Superseded Paddocks", "Planned Paddocks"],
        FeatureStatus.Built: ["Archived Paddocks", "Built Paddocks"]
    }

    def relayout(self):
        """Filter affected and resulting Paddock features by the selected Fence."""

        if self.fence is None:
            super().relayout()
            return

        for fenceStatus in [FeatureStatus.Drafted, FeatureStatus.Planned, FeatureStatus.Built]:
            if self.fence.matchStatus(fenceStatus):
                for i, paddocks in enumerate(self.fence.getRelatedPaddocks()):
                    if paddocks:
                        self.featureTable(i + 1).setVisible(True)
                        self.featureTable(i + 1).setTitle(self._PADDOCK_TABLE_TITLES[fenceStatus][i])
                        self.featureTable(i + 1).setFilteredFeatures([p.FID for p in paddocks])
                    else:
                        self.featureTable(i + 1).setVisible(False)

        super().relayout()
