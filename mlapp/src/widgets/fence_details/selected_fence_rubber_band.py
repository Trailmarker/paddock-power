# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QColor

from qgis.core import QgsWkbTypes
from qgis.gui import QgsRubberBand

from ...models.paddock_power_state import PaddockPowerState, connectPaddockPowerStateListener

class SelectedFenceRubberBand(QgsRubberBand):

    def __init__(self, canvas, parent=None):
        """Constructor."""
        super(QgsRubberBand, self).__init__(
            canvas, QgsWkbTypes.LineGeometry)

        self.selectedFence = None
        self.canvas = canvas

        self.state = PaddockPowerState()
        connectPaddockPowerStateListener(self.state, self)

        fenceColour = QColor("brown")
        # fenceColour.setAlphaF(0.8)
        self.setWidth(10)
        self.setColor(fenceColour)
        self.show()

    def refreshUi(self):
        """Refresh the Fence rubber band."""
        self.selectedFence = self.state.getSelectedFence()

        self.reset(QgsWkbTypes.LineGeometry)

        if self.selectedFence is not None:
            self.setToGeometry(self.selectedFence.geometry())

    @pyqtSlot()
    def onProjectChanged(self, project):
        self.refreshUi()

    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        self.refreshUi()

    @pyqtSlot()
    def onSelectedFenceChanged(self, fence):
        self.refreshUi()
