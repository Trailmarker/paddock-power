# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ...spatial.feature.fence import Fence, asFence
from ...models.paddock_power_error import PaddockPowerError
from ...models.paddock_power_state import PaddockPowerState, connectPaddockPowerStateListener

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_paddock_changes_base.ui')))


class FencePaddockChanges(QWidget, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.state = PaddockPowerState()
        connectPaddockPowerStateListener(self.state, self)

        self.fence = None

        self.refreshUi()

    @pyqtSlot()
    def onProjectChanged(self, project):
        """Handle a change in the current Paddock Power project."""
        self.clearFence()
        self.refreshUi()

    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        """Handle a change in the current Paddock Power milestone."""
        self.clearFence()
        self.refreshUi()

    @pyqtSlot()
    def onMilestoneDataChanged(self):
        """Handle a change to the underlying Milestone data."""
        self.clearFence()

        milestone = self.state.getMilestone()
        self.onSelectedFenceChanged(milestone.selectedFence)

    @pyqtSlot()
    def onSelectedFenceChanged(self, fence):
        """Handle a change in the selected fence."""
        self.clearFence()

        if fence is not None:
            fence = asFence(fence)
            milestone = self.state.getMilestone()
            milestone.paddockLayer.updateFencePaddocks(fence)
            self.setFence(fence)
            self.refreshUi()

    def refreshUi(self):
        """Show the Paddock View."""
        if self.fence is None:
            # self.setVisible(False)
            self.supersededPaddockMiniList.clear()
            self.plannedPaddockMiniList.clear()
        else:
            self.setVisible(True)
            self.supersededPaddockMiniList.setPaddocks(
                self.fence.supersededPaddocks)
            self.plannedPaddockMiniList.setPaddocks(self.fence.plannedPaddocks)

    def clearFence(self):
        self.fence = None
        self.supersededPaddocks = []
        self.plannedPaddocks = []

    def setFence(self, fence):
        if fence is not None and not isinstance(fence, Fence):
            raise PaddockPowerError(
                "FencePaddockChangesWidget.setFence: fence must be a Fence")

        if fence is None:
            self.clearFence()

        self.fence = fence
