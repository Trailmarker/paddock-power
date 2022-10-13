# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsFeature

from ...models.paddock_power_error import PaddockPowerError
from ...models.paddock_power_state import PaddockPowerState, connectPaddockPowerStateListener

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_paddock_changes_widget_base.ui')))


class FencePaddockChangesWidget(QWidget, FORM_CLASS):

    def __init__(self, fence, parent=None):
        """Constructor."""
        super(QWidget, self).__init__(parent)

        self.setupUi(self)

        self.state = PaddockPowerState()
        connectPaddockPowerStateListener(self.state, self)

        self.clearFence()
        self.setFence(fence)

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
    def onSelectedFenceChanged(self, fence):
        """Handle a change in the selected fence."""
        self.setFence(fence)

    def refreshUi(self):
        """Show the Paddock View."""
        self.supersededPaddockMiniList.setPaddocks(self.supersededPaddocks)
        self.plannedPaddockMiniList.setPaddocks(self.plannedPaddocks)

    def clearFence(self):
        self.fence = None
        self.supersededPaddocks = []
        self.plannedPaddocks = []

    def setFence(self, fence):
        if fence is not None and not isinstance(fence, QgsFeature):
            raise PaddockPowerError(
                "FencePaddockChangesWidget.setFence: fence must be a QgsFeature")
        
        if fence is None:
            self.clearFence()
        
        self.fence = fence
        milestone = self.state.getMilestone()
        if milestone is not None:
            paddockLayer = milestone.paddockLayer
            _, self.supersededPaddocks, self.plannedPaddocks = self.fence.analyseFence(paddockLayer)
        else:
            raise PaddockPowerError("FencePaddockChangesWidget.setFence: current milestone should not be empty")

        self.refreshUi()
