# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ...spatial.layers.mixins.interaction_mixin import InteractionMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_paddock_changes_base.ui')))


class FencePaddockChanges(QWidget, FORM_CLASS, InteractionMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        InteractionMixin.__init__(self)

        self.fence = None
        self.setupUi(self)
        self.refreshUi()

    def connectWorkspace(self, workspace):
        """Set the Workspace."""
        InteractionMixin.connectWorkspace(self, workspace)
        if self.workspace:
            self.supersededMetricPaddockMiniList.paddockLayer = self.workspace.paddockLayer
            self.plannedMetricPaddockMiniList.paddockLayer = self.workspace.paddockLayer
            self.workspace.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)
        self.refreshUi()

    def changeSelection(self, feature):
        InteractionMixin.changeSelection(self, feature)
        self.fence = feature
        self.fence.statusChanged = lambda _: self.refreshUi()
        
    def removeSelection(self):
        InteractionMixin.removeSelection(self)
        self.fence = None
        
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
