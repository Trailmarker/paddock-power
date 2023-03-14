# -*- coding: utf-8 -*-
from qgis.core import QgsGeometry, QgsWkbTypes
from qgis.gui import QgsRubberBand

from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor

from .map_tool import MapTool


class SketchPointTool(MapTool):
    sketchFinished = pyqtSignal(QgsGeometry)

    def __init__(self):

        super().__init__()

        # The point we'll sketch
        self.point = None

        # The points in a sketch
        self.points = []

        # A flag to know whether the tool is capturing a drawing
        self.capturing = False

        sketchColour = QColor("red")
        sketchColour.setAlphaF(0.8)
        self.sketch = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.sketch.setWidth(5)
        self.sketch.setColor(sketchColour)
        self.sketch.show()

    def clear(self):
        self.sketch.reset()

    def dispose(self):
        """Completely delete or destroy all graphics objects or other state associated with the tool."""
        self.canvas.scene().removeItem(self.sketch)
        super().dispose()

    def canvasPressEvent(self, e):
        """Handle the canvas press event."""
        if e.button() == Qt.LeftButton:
            # Clear the rubber band when we start
            if not self.capturing:
                self.clear()
                self.points = []

            # We are drawing now
            self.capturing = True
            pointXY = self.toMapCoordinates(e.pos())
            self.point = QgsGeometry.fromPointXY(pointXY)
            self.sketch.setToGeometry(self.point)

        if e.button() == Qt.RightButton:
            self.capturing = False
            self.workspace.unsetTool()
            self.updatePoint()

    def updatePoint(self):
        """Update the current fenceline profile based on the sketch."""
        self.sketchFinished.emit(self.point)
