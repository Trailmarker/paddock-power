# -*- coding: utf-8 -*-
from qgis.core import QgsGeometry, QgsFeature, QgsPoint, QgsWkbTypes
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.utils import iface

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor

from ..utils import qgsDebug

class SplitPaddock(QgsMapTool):
    points = []

    def __init__(self, canvas, milestone):
        
        QgsMapTool.__init__(self, canvas)
        
        self.canvas = canvas
        self.layer = milestone.paddockLayer

        # flag to know whether the tool is capturing a drawing 
        self.capturing = False

        sketchColour = QColor("red")
        sketchColour.setAlphaF(0.8)
        self.sketch = QgsRubberBand(self.canvas,QgsWkbTypes.LineGeometry)
        self.sketch.setWidth(2)
        self.sketch.setColor(sketchColour)
        self.sketch.show()

        guideColour = QColor("grey")
        guideColour.setAlphaF(0.8)
        self.guide = QgsRubberBand(self.canvas,QgsWkbTypes.LineGeometry)
        self.guide.setWidth(2)
        self.guide.setColor(guideColour)
        self.guide.setLineStyle(Qt.DashLine)
        self.guide.show()


    def clear(self):
        self.sketch.reset(False)
        self.guide.reset(False)

    # def delete(self):
    #     self.canvas.scene().removeItem(self.sketch)
    #     self.canvas.scene().removeItem(self.guide)

    def startCapturing(self):
        self.capturing = True

    def canvasMoveEvent(self, event):
        if self.guide is not None and self.capturing and self.points:
            l = self.points[-1]
            g = self.toMapCoordinates(event.pos())
            guideLine = QgsGeometry.fromPolyline([QgsPoint(l.x(),l.y()), QgsPoint(g.x(),g.y())])
            self.guide.setToGeometry(guideLine, None)

        
    def canvasPressEvent(self, e):
        # which the mouse button?
        if e.button() == Qt.LeftButton:
            # clear the rubber band when we start            
            if not self.capturing:
                qgsDebug("clearing rubberband")
                self.clear()
                self.points = []

            # we are drawing now
            self.capturing = True
            point = self.toMapCoordinates(e.pos())
 
            # add a new point to the rubber band
            self.points.append(QgsPoint(point))
            polyline = QgsGeometry.fromPolyline(self.points)
            self.sketch.setToGeometry(polyline)
            
        if e.button() == Qt.RightButton:
            self.capturing = False
            polyline = QgsGeometry.fromPolyline(self.points)

            

