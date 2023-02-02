# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ...layers.features import Fence
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

        self.supersededMetricPaddockMiniList.paddockLayer = self.paddockLayer
        self.plannedMetricPaddockMiniList.paddockLayer = self.paddockLayer

        self.fenceLayer.featureSelected.connect(self.changeSelection)
        self.refreshUi()

    @property
    def fenceLayer(self):
        return self.workspace.fenceLayer

    @property
    def paddockLayer(self):
        return self.workspace.paddockLayer

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
            # self.setVisible(False)
            self.supersededMetricPaddockMiniList.clear()
            self.plannedMetricPaddockMiniList.clear()
        else:
            # self.setVisible(True)
            supersededPaddocks, plannedPaddocks = self.fence.getCurrentAndFuturePaddocks()

            self.supersededMetricPaddockMiniList.setFeatures(supersededPaddocks)
            self.plannedMetricPaddockMiniList.setFeatures(plannedPaddocks)
