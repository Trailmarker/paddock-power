# -*- coding: utf-8 -*-
import matplotlib.pyplot as plot

from qgis.core import QgsGeometry, QgsPoint, QgsWkbTypes
from qgis.gui import QgsRubberBand

from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor

from ...models.milestone import Milestone
from ...models.project import Project
from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug
from ..paddock_power_map_tool import PaddockPowerMapTool
from .fenceline_profile import FencelineProfile
from .fenceline_profile_dialog import FencelineProfileDialog


class FencelineProfileTool(PaddockPowerMapTool):
    points = []

    fencelineProfileUpdated = pyqtSignal(FencelineProfile)

    def __init__(self, milestone, project):

        super(FencelineProfileTool, self).__init__()

        if not isinstance(milestone, Milestone):
            raise PaddockPowerError(
                "FencelineProfileTool.__init__: milestone is not a Milestone.")

        if not isinstance(project, Project):
            raise PaddockPowerError(
                "FencelineProfileTool.__init__: project is not a Project.")

        self.milestone = milestone
        self.project = project

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
        # self.dialog = FencelineProfileDialog(self.fencelineProfile)
        # self.dialog.exec_()
        
        # self.dialog.show()

    def clear(self):
        self.sketch.reset()
        self.guide.reset()

    def dispose(self):
        """Completely delete or destroy all graphics objects or other state associated with the tool."""
        self.canvas.scene().removeItem(self.sketch)
        self.canvas.scene().removeItem(self.guide)
        super(FencelineProfileTool, self).dispose()

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

            # self.updateFencelineAnalysis()

        if e.button() == Qt.RightButton:
            self.capturing = False
            self.milestone.unsetTool()
            self.updateFencelineProfile()
            # self.showDialog()

    def updateFencelineProfile(self):
        """Update the current fenceline profile based on the sketch."""
        qgsDebug("Updating fenceline profile …")
        fenceline = QgsGeometry.fromPolyline(self.points)
        fencelineProfile = FencelineProfile(fenceline, self.project.elevationLayer)
        self.fencelineProfileUpdated.emit(fencelineProfile)

