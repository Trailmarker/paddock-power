# -*- coding: utf-8 -*-
from qgis.core import QgsGeometry, QgsPoint
from qgis.gui import QgsMapTool, QgsRubberBand
from PyQt5.QtCore import Qt

class SketchLineTool(QgsMapTool):
    def __init__(self, canvas, layer):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.layer = layer

        self.rubber = QgsRubberBand(self.canvas, False)
        self.points = []

        self.setCursor(Qt.CrossCursor)

    def canvasReleaseEvent(self, event):
        point = self.toLayerCoordinates(self.layer, event.pos())

        self.points.append(QgsPoint(point))
        self.rubber.setToGeometry(QgsGeometry.fromPolyline(self.points), None)

        for point in self.points:
            print(point.x(), point.y())

        # print coordinates to console
        # print(point.x(), point.y())

        # after click, deactivate the tool
        # self.canvas.unsetMapTool(self)
