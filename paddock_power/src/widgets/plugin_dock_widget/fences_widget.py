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

        self.workspace.featureSelected.connect(self.selectFence)
        self.workspace.featureDeselected.connect(self.clearSelectedFence)

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
        fence = self.workspace.fenceLayer.makeFeature()
        fence.draftFeature(sketchLine)
        self.workspace.selectFeature(fence)

    def selectFence(self, layerId):
        if self.fenceLayer and layerId == self.fenceLayer.id():
            selectedFids = self.fenceLayer.selectedFeatureIds()

            if len(selectedFids) == 1:
                feature = self.fenceLayer.getFeature(selectedFids[0])
                if isinstance(feature, Fence):
                    self.fence = feature
                    self.relayout()

    def clearSelectedFence(self, layerId):
        if self.fenceLayer and layerId == self.fenceLayer.id():
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
                        self.setFeatureTableVisible(i + 1, True)
                        self.setFeatureTableTitle(i + 1, self._PADDOCK_TABLE_TITLES[fenceStatus][i])
                        self.setFeatureTableFilteredFeatures(i + 1, [p.FID for p in paddocks])
                    else:
                        self.setFeatureTableVisible(i + 1, False)

        super().relayout()
