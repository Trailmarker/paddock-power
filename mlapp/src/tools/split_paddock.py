# -*- coding: utf-8 -*-
from re import I
from ..models.paddock_power_error import PaddockPowerError
from qgis.core import QgsGeometry, QgsPoint, QgsWkbTypes
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.utils import iface

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor

from ..models.milestone import Milestone
from ..utils import qgsDebug


class SplitPaddock(QgsMapTool):
    points = []

    def __init__(self, canvas, milestone):
        if not isinstance(milestone, Milestone):
            raise PaddockPowerError(
                "SplitPaddock: milestone is not a Milestone object.")

        QgsMapTool.__init__(self, canvas)

        self.canvas = canvas
        self.milestone = milestone
        self.layer = milestone.paddockLayer

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

    # def delete(self):
    #     self.canvas.scene().removeItem(self.sketch)
    #     self.canvas.scene().removeItem(self.guide)

    def canvasMoveEvent(self, event):
        if self.guide is not None and self.capturing and self.points:
            l = self.points[-1]
            g = self.toMapCoordinates(event.pos())
            guideLine = QgsGeometry.fromPolyline(
                [QgsPoint(l.x(), l.y()), QgsPoint(g.x(), g.y())])
            self.guide.setToGeometry(guideLine, None)

    def canvasPressEvent(self, e):
        # which the mouse button?
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
            self.clear()

    def updatePaddockFeatures(self):
        """Update the currently crossed paddock features."""

        splitLine = QgsGeometry.fromPolyline(self.points)
        crossedPaddocks = self.layer.crossedPaddocks(splitLine)

        self.paddockFeatures.reset(QgsWkbTypes.PolygonGeometry)

        for paddock in crossedPaddocks:
            self.paddockFeatures.addGeometry(paddock.geometry(), None)

