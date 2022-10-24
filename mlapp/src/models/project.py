# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot

from qgis.core import QgsRectangle

from ..spatial.features.pipeline import Pipeline
from ..spatial.features.feature import Feature
from ..spatial.features.fence import Fence
from ..spatial.features.paddock import Paddock
from ..spatial.layers.feature_layer import FeatureLayer
from ..utils import qgsDebug
from ..views.infrastructure_view.infrastructure_view import InfrastructureView
from ..views.paddock_view.paddock_view import PaddockView
from ..widgets.fence_details.fence_selection import FenceSelection
from ..widgets.paddock_details.paddock_selection import PaddockSelection
from ..widgets.paddock_power_map_tool import PaddockPowerMapTool
from ..widgets.pipeline_details.pipeline_selection import PipelineSelection
from .glitch import Glitch
from .project_base import ProjectBase

# Initialize Qt resources from file resources.py
from ...resources_rc import *


class Project(ProjectBase):
    MENU_NAME = u"&Paddock Power"

    # emit this signal when a selected Feature is updated
    selectedFeatureChanged = pyqtSignal(Feature)
    projectDataChanged = pyqtSignal()
    projectUnloading = pyqtSignal()

    def __init__(self, iface, gpkgFile=None, projectName=None):
        super().__init__(gpkgFile, projectName)

        self.iface = iface

        self.currentTool = None

        self.selectedFeatures = {
            Fence: None,
            Paddock: None,
            Pipeline: None
        }

        canvas = self.iface.mapCanvas()

        # self.paddockSelection = PaddockSelection(self, canvas)
        # self.pipelineSelection = PipelineSelection(self, canvas)
        # self.fenceSelection = FenceSelection(self, canvas)

        self.views = {}

        for layer in [self.pipelineLayer, self.fenceLayer, self.paddockLayer]:
            layer.selectionChanged.connect(lambda selection, *_: self.onLayerSelectionChanged(layer, selection))
            layer.afterCommitChanges.connect(lambda: self.projectDataChanged.emit)

    @property
    def selectedFence(self):
        """Get the currently selected fence."""
        return self.selectedFeatures[Fence]

    @property
    def selectedPaddock(self):
        """Get the currently selected paddock."""
        return self.selectedFeatures[Paddock]

    @property
    def selectedPipeline(self):
        """Get the currently selected pipeline."""
        return self.selectedFeatures[Pipeline]

    def setTool(self, tool):
        """Set the current tool for this Project."""
        if not isinstance(tool, PaddockPowerMapTool):
            raise Glitch(
                "The Paddock Power tool must be of a recognised type")

        self.unsetTool()
        self.currentTool = tool
        self.iface.mapCanvas().setMapTool(self.currentTool)

    def unsetTool(self):
        if self.currentTool is not None:
            self.currentTool.clear()
            self.currentTool.dispose()
            self.iface.mapCanvas().unsetMapTool(self.currentTool)
            self.currentTool = None

    def selectFeature(self, feature):
        if feature is not None and not isinstance(feature, Feature):
            raise Glitch(
                "You can't select an object that is not a Feature")
        qgsDebug("Selecting feature: {}".format(feature))

        self.selectedFeatures[type(feature)] = feature
        self.selectedFeatureChanged.emit(feature)

    @pyqtSlot()
    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        self.projectUnloading.emit()

        self.unsetTool()

        # self.fenceSelection.cleanUp()
        # self.paddockSelection.cleanUp()
        # self.pipelineSelection.cleanUp()

        for viewType, view in self.views.values():
            self.iface.removeDockWidget(view)
            self.onCloseView(viewType)

    @pyqtSlot(Feature)
    def zoomFeature(self, feature):
        self.selectFeature(feature)

        if feature.geometry:
            featureExtent = QgsRectangle(feature.geometry.boundingBox())
            featureExtent.scale(1.5)  # Expand by 50%
            self.iface.mapCanvas().setExtent(featureExtent)
            self.iface.mapCanvas().refresh()

    @pyqtSlot(FeatureLayer, list)
    def onLayerSelectionChanged(self, layer, selection):
        if len(selection) == 1:
            feature = layer.getFeatureById(selection[0])
            qgsDebug(f"onLayerSelectionChanged: {feature or 'None'}")
            if feature is not None:
                self.selectFeature(feature)

    def openView(self, viewType, dockArea):
        if viewType not in self.views:
            view = viewType(self)
            view.closingView.connect(lambda: self.onCloseView(viewType))
            self.views[viewType] = view
            self.iface.addDockWidget(dockArea, view)
            view.show()

    @pyqtSlot()
    def openPaddockView(self):
        """Run method that loads and opens Paddock View."""
        self.openView(PaddockView, Qt.LeftDockWidgetArea)

    @pyqtSlot()
    def openInfrastructureView(self):
        """Run method that loads and opens Plan Fences and Pipelines."""
        self.openView(InfrastructureView, Qt.BottomDockWidgetArea)

    @pyqtSlot()
    def onCloseView(self, viewType):
        if viewType in self.views:
            del self.views[viewType]
