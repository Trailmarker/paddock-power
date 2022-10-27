# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot

from qgis.core import QgsRectangle

from ..spatial.features.fence import Fence
from ..spatial.features.paddock import Paddock
from ..spatial.features.persisted_feature import PersistedFeature
from ..spatial.features.pipeline import Pipeline
from ..spatial.layers.persisted_feature_layer import PersistedFeatureLayer
from ..tools.map_tool import MapTool
from ..views.fence_view.fence_view import FenceView
from ..views.paddock_view.paddock_view import PaddockView
from ..views.pipeline_view.pipeline_view import PipelineView
from ..views.waterpoint_view.waterpoint_view import WaterpointView
from .glitch import Glitch
from .project_base import ProjectBase

# Initialize Qt resources from file resources.py
from ...resources_rc import *


class Project(ProjectBase):
    MENU_NAME = u"&Paddock Power"

    # emit this signal when a selected Feature is updated
    selectedFeatureChanged = pyqtSignal(PersistedFeature)
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

        self.selectedFeatureChanged.connect(self.zoomFeature)

        self.pipelineLayer.selectionChanged.connect(lambda selection, *
                                                    _: self.onLayerSelectionChanged(self.pipelineLayer, selection))
        self.fenceLayer.selectionChanged.connect(lambda selection, *
                                                 _: self.onLayerSelectionChanged(self.fenceLayer, selection))
        self.paddockLayer.selectionChanged.connect(lambda selection, *
                                                   _: self.onLayerSelectionChanged(self.paddockLayer, selection))
        self.waterpointLayer.selectionChanged.connect(lambda selection, *
                                                      _: self.onLayerSelectionChanged(self.waterpointLayer, selection))

        # for layer in [self.pipelineLayer, self.fenceLayer, self.paddockLayer, self.waterpointLayer]:
        #     layer.selectionChanged.connect(lambda selection, *_: self.onLayerSelectionChanged(layer, selection))
        # layer.afterCommitChanges.connect(lambda: self.projectDataChanged.emit)

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
        if not isinstance(tool, MapTool):
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
        # qgsDebug(f"Project.selectFeature({feature})")
        self.selectedFeatures[feature.__class__.__name__] = feature
        self.selectedFeatureChanged.emit(feature)

    @pyqtSlot()
    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        self.projectUnloading.emit()

        self.unsetTool()

        for viewType, view in self.views.values():
            self.iface.removeDockWidget(view)
            self.onCloseView(viewType)

    @pyqtSlot(PersistedFeature)
    def zoomFeature(self, feature):

        if feature.geometry:
            featureExtent = QgsRectangle(feature.geometry.boundingBox())
            featureExtent.scale(1.5)  # Expand by 50%
            self.iface.mapCanvas().setExtent(featureExtent)
            self.iface.mapCanvas().refresh()

    @pyqtSlot(PersistedFeatureLayer, list)
    def onLayerSelectionChanged(self, layer, selection):
        # qgsDebug(f"Project.onLayerSelectionChanged({layer.__class__.__name__}, {selection})")

        if len(selection) == 1:
            feature = layer.getFeature(selection[0])
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
    def openFenceView(self):
        """Run method that loads and opens Plan Fences and Pipelines."""
        self.openView(FenceView, Qt.BottomDockWidgetArea)

    @pyqtSlot()
    def openPaddockView(self):
        """Run method that loads and opens Paddock View."""
        self.openView(PaddockView, Qt.LeftDockWidgetArea)

    @pyqtSlot()
    def openPipelineView(self):
        """Run method that loads and opens Plan Fences and Pipelines."""
        self.openView(PipelineView, Qt.BottomDockWidgetArea)

    @pyqtSlot()
    def openWaterpointView(self):
        """Run method that loads and opens Plan Fences and Pipelines."""
        self.openView(WaterpointView, Qt.BottomDockWidgetArea)

    @pyqtSlot()
    def onCloseView(self, viewType):
        if viewType in self.views:
            del self.views[viewType]
