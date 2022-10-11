# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDockWidget, QSizePolicy


from ...models.state import detectProject, getMilestone, getProject, getState
from ...utils import guiError, qgsDebug
from .infrastructure_profile_canvas import InfrastructureProfileCanvas
from .infrastructure_profile_tool import InfrastructureProfileTool

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'infrastructure_profile_dock_widget_base.ui')))


class InfrastructureProfileDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()
    refreshUiNeeded = pyqtSignal()

    fencelineProfile = None
    fencelineProfileCanvas = None

    def __init__(self, parent=None):
        """Constructor."""
        super(QDockWidget, self).__init__(parent)

        self.setupUi(self)

        # self.sketchFencelineButton.setIcon(
        #     QIcon(":/plugins/mlapp/images/new-split-paddock.png"))
        # self.selectFencelineButton.setIcon(
        #     QIcon(":/plugins/mlapp/images/new-split-paddock.png"))

        self.sketchFencelineButton.clicked.connect(self.sketchFenceline)

        detectProject()

        getState().projectChanged.connect(self.setupConnections)
        getState().projectChanged.connect(self.render)
        self.refreshUiNeeded.connect(self.render)

        self.render()

    def setupConnections(self):
        """Reconnect things as necessary."""
        project = getProject()
        if project is not None:
            project.currentMilestoneChanged.connect(self.render)

    def showEvent(self, event):
        detectProject()

    def sketchFenceline(self):
        """Set InfrastructureProfileTool as a custom map tool."""
        milestone = getMilestone()

        if milestone is None:
            guiError(
                "Please set the current Milestone before using the Plan Fences and Pipelines tool.")
        else:
            project = getProject()
            tool = InfrastructureProfileTool(milestone, project)
            tool.fencelineProfileUpdated.connect(self.setInfrastructureProfile)
            milestone.setTool(tool)

    def setInfrastructureProfile(self, fencelineProfile):
        """Set the Plan Fences and Pipelines."""
     
        qgsDebug("Fenceline profile is being updated in dock widget …")
        self.fencelineProfile = fencelineProfile
        self.refreshUiNeeded.emit()


    def refreshUi(self):
        """Show the Plan Fences and Pipelines."""


        if self.fencelineProfileCanvas is not None:
            # self.gridLayout.removeWidget(self.fencelineProfileCanvas)
            self.gridLayout.addWidget(self.placeholderLabel, 4, 0, 1, 4)

        if self.fencelineProfile is not None:
            useMetres = (self.fencelineProfile.maximumDistance < 1000)

            maximumDistance = self.fencelineProfile.maximumDistance if useMetres else self.fencelineProfile.maximumDistance / 1000
            self.elevationStats.setText(
                f"{self.fencelineProfile.minimumElevation:,.0f} – {self.fencelineProfile.maximumElevation:,.0f}m (mean {self.fencelineProfile.meanElevation})")

            if useMetres:
                self.fencelineLength.setText(f"{maximumDistance:,.0f}m")
            else:
                self.fencelineLength.setText(f"{maximumDistance:,.2f}km")

            self.fencelineProfileCanvas = InfrastructureProfileCanvas(self.fencelineProfile)
            self.fencelineProfileCanvas.setSizePolicy(QSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.Maximum))

            self.fencelineProfileCanvas.setMaximumHeight(250)
            # self.fencelineProfileCanvas.resize(1000,1000)

            # self.dockWidgetContents.setStyleSheet("background-color:red;")
            # self.gridLayout.removeWidget(self.placeholderLabel)
            self.gridLayout.addWidget(self.fencelineProfileCanvas, 4, 0, 1, 4)

            



    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
