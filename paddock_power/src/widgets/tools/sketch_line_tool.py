# -*- coding: utf-8 -*-
from qgis.core import QgsGeometry, QgsPoint, QgsWkbTypes
from qgis.gui import QgsRubberBand

from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor

from .map_tool import MapTool


class SketchLineTool(MapTool):
    sketchFinished = pyqtSignal(QgsGeometry)

    def __init__(self):

        super().__init__()

        self.points = []

        # A flag to know whether the tool is capturing a drawing
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

    def clear(self):
        self.sketch.reset()
        self.guide.reset()

    def dispose(self):
        """Completely delete or destroy all graphics objects or other state associated with the tool."""
        self.canvas.scene().removeItem(self.sketch)
        self.canvas.scene().removeItem(self.guide)
        super().dispose()

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
            # Clear the rubber band when we start
            if not self.capturing:
                self.clear()
                self.points = []

            # We are drawing now
            self.capturing = True
            point = self.toMapCoordinates(e.pos())

            # Add a new point to the rubber band
            self.points.append(QgsPoint(point))
            polyline = QgsGeometry.fromPolyline(self.points)
            self.sketch.setToGeometry(polyline)

        if e.button() == Qt.RightButton:
            self.capturing = False
            self.workspace.unsetTool()
            self.updateLine()

    def updateLine(self):
        """Update the current fenceline profile based on the sketch."""
        sketchLine = QgsGeometry.fromPolyline(self.points)

        self.sketchFinished.emit(sketchLine)
