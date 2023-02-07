# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ...layers.features import Fence
from ...layers.fields.feature_status import FeatureStatus
from ...models import WorkspaceMixin
from ...utils import qgsDebug

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_paddock_changes_base.ui')))


class FencePaddockChanges(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.fence = None
        self.setupUi(self)

        self.affectedPaddockMiniList.basePaddockLayer = self.basePaddockLayer
        self.resultingPaddockMiniList.basePaddockLayer = self.basePaddockLayer

        self.fenceLayer.featureSelected.connect(self.changeSelection)
        self.refreshUi()

    @property
    def fenceLayer(self):
        return self.workspace.fenceLayer

    @property
    def basePaddockLayer(self):
        return self.workspace.basePaddockLayer

    def changeSelection(self, layerType):
        qgsDebug("FencePaddockChanges.changeSelection")
        feature = self.workspace.selectedFeature(layerType)
        qgsDebug(f"FencePaddockChanges.changeSelection: feature = {feature}")

        if isinstance(feature, Fence):
            self.fence = feature
            self.refreshUi()

    def removeSelection(self):
        self.fence = None
        self.refreshUi()

    def refreshUi(self):
        """Show the Paddock View."""
        if self.fence is None:
            self.setVisible(False)
            self.affectedPaddockMiniList.clear()
            self.resultingPaddockMiniList.clear()
        else:
            self.setVisible(True)
            affectedPaddocks, resultingPaddocks = self.fence.getRelatedPaddocks()

            if self.fence.matchStatus(FeatureStatus.Drafted):
                self.affectedPaddockGroupBox.setTitle("Crossed Paddocks")
                self.resultingPaddockGroupBox.setTitle("New Paddocks")
            elif self.fence.matchStatus(FeatureStatus.Planned):
                self.affectedPaddockGroupBox.setTitle("Superseded Paddocks")
                self.resultingPaddockGroupBox.setTitle("Planned Paddocks")
            elif self.fence.matchStatus(FeatureStatus.Built):
                self.affectedPaddockGroupBox.setTitle("Archived Paddocks")
                self.resultingPaddockGroupBox.setTitle("Built Paddocks")

            # Hide these Paddock group boxes if there's no content
            self.affectedPaddockGroupBox.setVisible(bool(affectedPaddocks))
            self.resultingPaddockGroupBox.setVisible(bool(resultingPaddocks))
            self.affectedPaddockMiniList.setFeatures(affectedPaddocks)
            self.resultingPaddockMiniList.setFeatures(resultingPaddocks)
