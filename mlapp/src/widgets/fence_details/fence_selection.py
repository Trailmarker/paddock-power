# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QColor

from qgis.core import QgsWkbTypes
from qgis.gui import QgsRubberBand

from ...spatial.selection import Selection


class FenceSelection(Selection):

    def __init__(self, canvas, parent=None):
        """Constructor."""
        super().__init__(canvas, QgsWkbTypes.LineGeometry)

        self.styleUi()

    def styleUi(self):
        """Style the rubber band."""
        backgroundColour = QColor("black")
        self.setWidth(10)
        self.setColor(backgroundColour)
        self.show()

        self.foregroundRubberBand = QgsRubberBand(
            self.canvas, QgsWkbTypes.LineGeometry)
        fenceColour = QColor("brown")
        self.foregroundRubberBand.setWidth(8)
        self.foregroundRubberBand.setColor(fenceColour)
        self.foregroundRubberBand.show()

    @pyqtSlot()
    def cleanUp(self):
        """Clean up the selection."""
        self.foregroundRubberBand.hide()
        self.foregroundRubberBand.reset(self.wkbType)
        self.canvas.scene().removeItem(self.foregroundRubberBand)

        super().cleanUp()

    def updateGeometry(self, geometry):
        """Set the rubber band to a geometry."""
        super().updateGeometry(geometry)

        self.foregroundRubberBand.reset(self.wkbType)
        if geometry is None:
            return
        self.foregroundRubberBand.setToGeometry(geometry, None)
