# -*- coding: utf-8 -*-
from qgis.core import QgsApplication, QgsGeometry, QgsPoint, QgsWkbTypes
from qgis.gui import QgsRubberBand
from qgis.utils import iface

from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtGui import QColor

from ...models.milestone import Milestone, PaddockPowerError
from ...utils import qgsDebug
from ..paddock_power_map_tool import PaddockPowerMapTool

class PlanInfrastructureTool(PaddockPowerMapTool):
    points = []

    def __init__(self, milestone, planningFence=True):

        super(PlanInfrastructureTool, self).__init__()

        if not isinstance(milestone, Milestone):
            raise PaddockPowerError(
                "PlanInfrastructureTool.__init__: milestone is not a Milestone.")

        self.milestone = milestone
        self.planningFence = planningFence

        # flag to know whether the tool is capturing a drawing
        self.capturing = False

        paddockColour = QColor("green")
        paddockColour.setAlphaF(0.8)
        self.paddockFeatures = QgsRubberBand(
            self.canvas, QgsWkbTypes.PolygonGeometry)
        self.paddockFeatures.setWidth(2)
        self.paddockFeatures.setColor(paddockColour)
        self.paddockFeatures.setFillColor(paddockColour)
        self.paddockFeatures.show()

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

        # QgsApplication.instance().focusChanged.connect(self.showDialogIfMainWindowActive)

    #    self.showDialog()

    # def showDialog(self):
    #     """Show the Split Paddock dialog."""
    #     self.dialog = PlanInfrastructureDialog(self)
    #     self.dialog.setWindowFlags(
    #         Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    #     # Move to top left corner of map
    #     # See https://gis.stackexchange.com/questions/342728/getting-screen-coordinates-from-canvas-coordinate-using-pyqgis
    #     point = self.canvas.mapToGlobal(QPoint(0, 0))
    #     self.dialog.move(point.x() + 10, point.y() + 10)

    #     self.dialog.show()

    def clear(self):
        self.sketch.reset()
        self.guide.reset()
        self.paddockFeatures.reset(QgsWkbTypes.PolygonGeometry)

    def dispose(self):
        """Completely delete or destroy all graphics objects or other state associated with the tool."""
        self.canvas.scene().removeItem(self.sketch)
        self.canvas.scene().removeItem(self.guide)
        self.canvas.scene().removeItem(self.paddockFeatures)
        super(PlanInfrastructureTool, self).dispose()

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

            self.updateCrossedPaddocks()

        # if e.button() == Qt.RightButton:
        #     self.capturing = False
        #     self.milestone.unsetTool()

    def finishPlanningInfrastructure(self):
        """Finish planning infrastructure."""
        self.milestone.unsetTool()

    def planInfrastructureLine(self):
        """Add the current sketch as a proposed fence."""

        if self.planningFence:
            self.milestone.fenceLayer.planFence(self.getInfrastructureLine())
        else:
            self.milestone.pipelineLayer.planPipeline(self.getInfrastructureLine())

        self.finishPlanningInfrastructure()

    def getInfrastructureLine(self):
        """Return the current split line."""
        return QgsGeometry.fromPolyline(self.points)

    def updateCrossedPaddocks(self):
        """Update the currently crossed paddock features."""

        crossedPaddocks, croppedSplitLine = self.milestone.paddockLayer.crossedPaddocks(
            self.getInfrastructureLine())

        self.paddockFeatures.reset(QgsWkbTypes.PolygonGeometry)

        for paddock in crossedPaddocks:
            self.paddockFeatures.addGeometry(paddock.geometry(), None)

        # self.dialog.setFenceLength(croppedSplitLine.length())
        self.sketch.setToGeometry(croppedSplitLine)
