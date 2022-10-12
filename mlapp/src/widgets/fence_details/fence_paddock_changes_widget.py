# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsFeature

from ...models.paddock_power_error import PaddockPowerError
from ...models.state import getMilestone
from ...utils import guiConfirm, qgsDebug

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_paddock_changes_widget_base.ui')))

class FencePaddockChangesWidget(QWidget, FORM_CLASS):

    refreshUiNeeded = pyqtSignal()

    def __init__(self, fence, parent=None):
        """Constructor."""
        super(QWidget, self).__init__(parent)

        self.setupUi(self)

        self.refreshUiNeeded.connect(self.refreshUi)
        self.existingPaddocks = []
        self.plannedPaddocks = []
        self.setFence(fence)

    def refreshUi(self):
        """Show the Paddock View."""
        self.existingPaddockMiniList.setPaddocks(self.existingPaddocks)
        self.plannedPaddockMiniList.setPaddocks(self.plannedPaddocks)

    def refreshPaddockChanges(self):
        """Refresh the paddock changes."""
        milestone = getMilestone()
        if milestone is not None:
            paddockLayer = milestone.paddockLayer
            croppedFenceLine, self.existingPaddocks, self.plannedPaddocks = paddockLayer.planFenceLine(self.fence.geometry())
            self.fence.setGeometry(croppedFenceLine)
            
    def setFence(self, fence):
        if fence is None or not isinstance(fence, QgsFeature):
            raise PaddockPowerError("FencePaddockChangesWidget.setFence: fence must be a QgsFeature")
        self.fence = fence
        self.refreshPaddockChanges()
        self.refreshUiNeeded.emit()
