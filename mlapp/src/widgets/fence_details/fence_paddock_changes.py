# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ...spatial.features.fence import Fence
from ...models.glitch import Glitch
from ...models.state import State, connectStateListener

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_paddock_changes_base.ui')))


class FencePaddockChanges(QWidget, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.state = State()
        connectStateListener(self.state, self)

        self.fence = None

        self.refreshUi()

    @pyqtSlot()
    def onProjectChanged(self, project):
        """Handle a change in the current Paddock Power project."""
        self.clearFence()

        if project is not None:
            self.onSelectedFeatureChanged(project.selectedFence)

    @pyqtSlot()
    def onMilestoneDataChanged(self):
        """Handle a change to the underlying Milestone data."""
        fence = self.state.getProject().selectedFence
        self.onSelectedFeatureChanged(fence)

    @pyqtSlot()
    def onSelectedFeatureChanged(self, fence):
        """Handle a change in the selected fence."""
        self.clearFence()

        if fence is not None and isinstance(fence, Fence):
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
            supersededPaddocks, plannedPaddocks = self.fence.getSupersededAndPlannedPaddocks()

            self.supersededPaddockMiniList.setFeatures(supersededPaddocks)
            self.plannedPaddockMiniList.setFeatures(plannedPaddocks)

    def clearFence(self):
        if self.fence is not None:
            self.fence.stateChanged.disconnect(self.refreshUi)
            self.fence = None
        self.supersededPaddocks = []
        self.plannedPaddocks = []

    def setFence(self, fence):
        if fence is not None and not isinstance(fence, Fence):
            raise Glitch(
                "FencePaddockChangesWidget.setFence: fence must be a Fence")

        if fence is None:
            self.clearFence()

        self.fence = fence
        self.fence.stateChanged.connect(self.refreshUi)
