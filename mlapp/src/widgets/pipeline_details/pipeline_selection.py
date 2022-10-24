# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QColor

from qgis.core import QgsWkbTypes
from qgis.gui import QgsRubberBand

from ...spatial.features.feature import Feature
from ...spatial.features.pipeline import Pipeline
from ...spatial.selection import Selection


class PipelineSelection(Selection):

    def __init__(self, project, canvas):
        """Constructor."""
        super().__init__(project, canvas, QgsWkbTypes.LineGeometry)

        self.styleUi()

    def styleUi(self):
        """Style the rubber band."""
        backgroundColour = QColor("black")
        self.setWidth(10)
        self.setColor(backgroundColour)
        self.show()

        self.foregroundRubberBand = QgsRubberBand(
            self.canvas, QgsWkbTypes.LineGeometry)
        fenceColour = QColor("purple")
        self.foregroundRubberBand.setWidth(8)
        self.foregroundRubberBand.setColor(fenceColour)
        self.foregroundRubberBand.show()

    def updateGeometry(self, geometry):
        """Set the rubber band to a geometry."""
        super().updateGeometry(geometry)

        self.foregroundRubberBand.reset(self.wkbType)
        if geometry is None:
            return
        self.foregroundRubberBand.setToGeometry(geometry, None)

    @pyqtSlot()
    def cleanUp(self):
        """Clean up the selection."""
        self.foregroundRubberBand.hide()
        self.foregroundRubberBand.reset(self.wkbType)
        self.canvas.scene().removeItem(self.foregroundRubberBand)

        super().cleanUp()

    @pyqtSlot(Feature)
    def setSelectedFeature(self, feature):
        if isinstance(feature, Pipeline):
            super().setSelectedFeature(feature)
