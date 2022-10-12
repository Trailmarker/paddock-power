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

        self.existingPaddocks = []
        self.plannedPaddocks = []
        self.setFence(fence)

    @pyqtSlot()
    def onProjectChanged(self, project):
        """Handle a change in the current Paddock Power project."""
        self.refreshUi()
    
    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        """Handle a change in the current Paddock Power milestone."""
        self.refreshUi()

    @pyqtSlot()
    def onMilestonesUpdated(self, milestones):
        """Handle a change to the current collection of Paddock Power milestones."""
        pass

    def refreshUi(self):
        """Show the Paddock View."""
        self.existingPaddockMiniList.setPaddocks(self.existingPaddocks)
        self.plannedPaddockMiniList.setPaddocks(self.plannedPaddocks)

    def refreshPaddockChanges(self):
        """Refresh the paddock changes."""
        milestone = self.state.getMilestone()
        if milestone is not None:
            paddockLayer = milestone.paddockLayer
            croppedFenceLine, self.existingPaddocks, self.plannedPaddocks = paddockLayer.planFenceLine(self.fence.geometry())
            self.fence.setGeometry(croppedFenceLine)
        else:
            self.existingPaddocks = []
            self.plannedPaddocks = []
            self.fence = None
        self.refreshUi()
            
    def setFence(self, fence):
        if fence is not None and not isinstance(fence, QgsFeature):
            raise PaddockPowerError("FencePaddockChangesWidget.setFence: fence must be a QgsFeature")
        self.fence = fence
        self.refreshPaddockChanges()
        self.refreshUi()
