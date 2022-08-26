# -*- coding: utf-8 -*-
import matplotlib.pyplot as plot
import processing

from qgis.core import QgsApplication, QgsDistanceArea, QgsGeometry, QgsPoint, QgsRasterLayer, QgsVectorLayer, QgsWkbTypes
from qgis.gui import QgsRubberBand
from qgis.utils import iface

from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtGui import QColor

# from .fenceline_analysis_dialog import FencelineAnalysisDialog
from ...models.milestone import Milestone, PaddockPowerError
from ..paddock_power_map_tool import PaddockPowerMapTool
from ...utils import qgsDebug


class FencelineAnalysisTool(PaddockPowerMapTool):
    points = []

    def __init__(self, milestone):

        super(PaddockPowerMapTool, self).__init__()

        if not isinstance(milestone, Milestone):
            raise PaddockPowerError(
                "FencelineAnalysisTool.__init__: milestone is not a Milestone.")

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


    def showDialog(self):
        """Show the Fenceline Analysis dialog."""
        # self.dialog = FencelineAnalysisDialog(self)
        # self.dialog.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Move to top left corner of map
        # See https://gis.stackexchange.com/questions/342728/getting-screen-coordinates-from-canvas-coordinate-using-pyqgis
        # point = self.canvas.mapToGlobal(QPoint(0, 0))
        # self.dialog.move(point.x() + 10, point.y() + 10)

        # self.dialog.show()

        # Plot some sample data
        listOfZValues = self.listOfZValues
        listOfDistances = self.distancesList

        minimumZValue = round(min(listOfZValues), 3)
        maximumZValue = round(max(listOfZValues), 3)
        meanZValue = round(sum(listOfZValues) / len(listOfZValues), 3)
        maximumDistance = listOfDistances[-1]
        plot.figure(figsize = (10,4))
        plot.plot(listOfDistances, listOfZValues)
        plot.plot([0, maximumDistance], [minimumZValue, minimumZValue],
                  'g--', label='Min. : '+str(minimumZValue))
        plot.plot([0, maximumDistance], [maximumZValue, maximumZValue],
                  'r--', label='Max. : '+str(maximumZValue))
        plot.plot([0, maximumDistance], [meanZValue, meanZValue], 'y--', label='Mean : ' + str(meanZValue))
        plot.grid()
        plot.legend(loc = 1)
        plot.xlabel("Distance (km)")
        plot.ylabel("Elevation (m)")
        plot.fill_between(listOfDistances, listOfZValues, minimumZValue, alpha=0.5)
        plot.show()

    def clear(self):
        self.sketch.reset()
        self.guide.reset()

    def dispose(self):
        """Completely delete or destroy all graphics objects or other state associated with the tool."""
        self.canvas.scene().removeItem(self.sketch)
        self.canvas.scene().removeItem(self.guide)
        super(FencelineAnalysisTool, self).dispose()

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

            self.updateFencelineAnalysis()

        if e.button() == Qt.RightButton:
            self.capturing = False
            self.milestone.unsetTool()
            self.showDialog()

    def getFenceline(self):
        """Return the current split line."""
        return QgsGeometry.fromPolyline(self.points)

    def updateFencelineAnalysis(self):
        """Update the currently crossed paddock features."""

        fenceline = self.getFenceline()

        # See https://www.geodose.com/2021/02/python-qgis-tutorial-create-elevation-profile.html

        # Change these  
        # dataDir = 'E:/Project/'  
        # elevationData = dataDir + 'lidar_dem.tif' 
        # analysisLine = dataDir + 'line_path.gpkg' 
        # fencePoints = dataDir + 'out_points.gpkg' 
        # fencePointsWithZ = dataDir + 'point_z.gpkg' 
   
        # Define raster layer and get cell resolution
        # elevationLayer = QgsRasterLayer(elevationData,'ogr')
        # interval = elevationLayer.rasterUnitsPerPixelX()

        # Processing using SAGA and GRASS
        # Convert input line to points … (shouldn't need to do this)
        # processing.run("grass7:v.to.points", {
        #     'input': analysisLine,
        #     'use': 1,
        #     'dmax': interval,
        #     '-i': True,
        #     '-t': False,
        #     'output': fencePoints
        # })

        # Add elevation values from DEM in project to points
        # processing.run("saga:addrastervaluestopoints", {
        #     'SHAPES': fencePoints, 
        #     'GRIDS': [elevationLayer],
        #     'RESAMPLING': 0,
        #     'RESULT': fencePointsWithZ
        # })

        # fencePointsWithZLayer = QgsVectorLayer(fencePointsWithZ,'ogr')

        # features = fencePointsWithZLayer.getFeatures()
        # first = next(features)
        # firstPoint = first.geometry().asPoint()
        # firstZValue = first.attributes()[-1]

        # Curate the points to use QgsDistanceArea on them
        # Empty dictionary
        # fromPoint = firstPoint
        # toPoint = None
        # distancesList = [0]
        # self.listOfZValues = [firstZValue]

        # Calculate distances using the GDA2020 ellipsoid 
        # distanceAreaCalculator = QgsDistanceArea()
        # distanceAreaCalculator.setEllipsoid('GDA202') # Note: example uses 'NAD83'

        # Get the Z value for each point
        # for f in features:
        #     zValue = f.attributes()[-1]
        #     self.listOfZValues.append(zValue)
        #     toPoint = f.geometry().asPoint()
        #     distance = distanceAreaCalculator.measureLine(fromPoint, toPoint)
        #     accumulatedLengthAtLineSegment = distance + distancesList[-1]
        #     distancesList.append(accumulatedLengthAtLineSegment)
        #     fromPoint = toPoint

        self.distancesList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.listOfZValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
