# -*- coding: utf-8 -*-
from qgis.core import QgsGeometry, QgsPoint
from qgis.gui import QgsMapTool, QgsRubberBand
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class SketchLineTool(QgsMapTool):
    def __init__(self, canvas, layer):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.layer = layer

        self.rubber = QgsRubberBand(self.canvas, False)
        self.rubber.setColor(QColor(255, 0, 0, 200))
        self.rubber.setFillColor(QColor(255, 0, 0, 40))
        self.rubber.setWidth(3)
        
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
