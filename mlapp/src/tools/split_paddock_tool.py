# -*- coding: utf-8 -*-
from qgis.core import QgsGeometry, QgsPoint, QgsWkbTypes
from qgis.gui import QgsRubberBand

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor

from ..models.milestone import Milestone, PaddockPowerError
from .paddock_power_map_tool import PaddockPowerMapTool
from ..utils import qgsDebug

class SplitPaddockTool(PaddockPowerMapTool):
    points = []

    def __init__(self, milestone):

        super(SplitPaddockTool, self).__init__()

        if not isinstance(milestone, Milestone):
            raise PaddockPowerError("SplitPaddockTool.__init__: milestone is not a Milestone.")

        self.milestone = milestone

        # flag to know whether the tool is capturing a drawing
        self.capturing = False

        sketchColour = QColor("red")
        sketchColour.setAlphaF(0.8)
        self.sketch = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.sketch.setWidth(2)
        self.sketch.setColor(sketchColour)
        self.sketch.show()

        guideColour = QColor("grey")
        guideColour.setAlphaF(0.8)
        self.guide = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.guide.setWidth(2)
        self.guide.setColor(guideColour)
        self.guide.setLineStyle(Qt.DashLine)
        self.guide.show()

        paddockColour = QColor("green")
        paddockColour.setAlphaF(0.8)
        self.paddockFeatures = QgsRubberBand(
            self.canvas, QgsWkbTypes.PolygonGeometry)
        self.paddockFeatures.setWidth(2)
        self.paddockFeatures.setColor(paddockColour)
        self.paddockFeatures.setFillColor(paddockColour)
        self.paddockFeatures.show()

    def clear(self):
        self.sketch.reset()
        self.guide.reset()
        self.paddockFeatures.reset(QgsWkbTypes.PolygonGeometry)

    def destroy(self):
        self.canvas.scene().removeItem(self.sketch)
        self.canvas.scene().removeItem(self.guide)
        self.canvas.scene().removeItem(self.paddockFeatures)

    def canvasMoveEvent(self, event):
        """Handle the canvas move event."""
        if self.guide is not None and self.capturing and self.points:
            l = self.points[-1]
            g = self.toMapCoordinates(event.pos())
            guideLine = QgsGeometry.fromPolyline(
                [QgsPoint(l.x(), l.y()), QgsPoint(g.x(), g.y())])
            self.guide.setToGeometry(guideLine, None)

    def canvasPressEvent(self, e):
        """Handle the canvas press event."""
        if e.button() == Qt.LeftButton:
            # clear the rubber band when we start
            if not self.capturing:
                self.clear()
                self.points = []

            # we are drawing now
            self.capturing = True
            point = self.toMapCoordinates(e.pos())

            # add a new point to the rubber band
            self.points.append(QgsPoint(point))
            polyline = QgsGeometry.fromPolyline(self.points)
            self.sketch.setToGeometry(polyline)

            self.updatePaddockFeatures()

        if e.button() == Qt.RightButton:
            self.capturing = False
            self.milestone.unsetTool()

    def updatePaddockFeatures(self):
        """Update the currently crossed paddock features."""

        splitLine = QgsGeometry.fromPolyline(self.points)
        crossedPaddocks = self.milestone.paddockLayer.crossedPaddocks(splitLine)

        self.paddockFeatures.reset(QgsWkbTypes.PolygonGeometry)

        for paddock in crossedPaddocks:
            self.paddockFeatures.addGeometry(paddock.geometry(), None)
