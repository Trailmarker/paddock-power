# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QColor

from qgis.core import QgsWkbTypes
from qgis.gui import QgsRubberBand

from ...models.paddock_power_state import PaddockPowerState, connectPaddockPowerStateListener
from ...utils import qgsDebug


class SelectedPaddockRubberBand(QgsRubberBand):

    def __init__(self, canvas, parent=None):
        """Constructor."""
        super(QgsRubberBand, self).__init__(
            canvas, QgsWkbTypes.PolygonGeometry)

        self.selectedPaddock = None
        self.canvas = canvas

        self.state = PaddockPowerState()
        connectPaddockPowerStateListener(self.state, self)

        paddockColour = QColor("green")
        paddockColour.setAlphaF(0.8)

        self.setWidth(2)
        self.setColor(paddockColour)
        self.setFillColor(paddockColour)

    def refreshUi(self):
        """Refresh the paddock rubber band."""
        self.selectedPaddock = self.state.getSelectedPaddock()

        self.reset(QgsWkbTypes.PolygonGeometry)

        if self.selectedPaddock is not None:
            self.addGeometry(self.selectedPaddock.geometry(), None)

    @pyqtSlot()
    def onProjectChanged(self, project):
        self.refreshUi()

    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        self.refreshUi()

    @pyqtSlot()
    def onSelectedPaddockChanged(self, paddock):
        self.refreshUi()
