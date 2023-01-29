# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, Qt, pyqtSignal, pyqtSlot

from qgis.core import QgsProject

from ..spatial.features.feature import Feature
from ..spatial.layers.derived_boundary_layer import DerivedBoundaryLayer
from ..spatial.layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.feature_layer import FeatureLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.land_type_layer import LandTypeLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.watered_area_layer import WateredAreaLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer
from ..spatial.fields.timeframe import Timeframe
from ..tools.map_tool import MapTool
from ..utils import PLUGIN_NAME
from ..views.feature_view.feature_view import FeatureView
from ..widgets.import_dialog.import_dialog import ImportDialog
from .glitch import Glitch
from .layer_dependency_graph import LayerDependencyGraph
from .workspace_layers import WorkspaceLayers

# Initialize Qt resources from file resources.py
from ...resources_rc import *


class Workspace(QObject):
    # emit this signal when a selected PersistedFeature is updated
    selectedFeaturesChanged = pyqtSignal(list)
    currentTimeframeChanged = pyqtSignal(Timeframe)
    workspaceUnloading = pyqtSignal()

    def __init__(self,
                 iface,
                 workspaceFile: str,
                 workspaceLayers: WorkspaceLayers):
        super().__init__(iface.mainWindow())

        self.workspaceName = PLUGIN_NAME

        self.workspaceFile = workspaceFile
        self.workspaceLayers = workspaceLayers
        self.layerDependencyGraph = LayerDependencyGraph()
            
        self.iface = iface
        self.currentTool = None
        self.currentTimeframe = Timeframe.Current
        self.views = {}
        self.importDialog = None
        self.selectedFeature = None

        self.currentTimeframeChanged.connect(self.deselectFeature)

        # For convenient reference
        [self.landTypeLayer,
         self.conditionTable,
         self.paddockLayer,
         self.elevationLayer,
         self.waterpointLayer,
         self.derivedWaterpointBufferLayer,
         self.waterpointBufferLayer,
         self.derivedWateredAreaLayer,
         self.wateredAreaLayer,
         self.derivedPaddockLandTypesLayer,
         self.paddockLandTypesLayer,
         self.derivedMetricPaddockLayer,
         self.fenceLayer,
         self.pipelineLayer,
         self.derivedBoundaryLayer] = [self.workspaceLayer(layerType) for layerType in self.layerDependencyGraph.loadOrder()]

        self.addToMap()


    def workspaceLayer(self, layerType):
        """Retrieve a layer by type."""
        return self.workspaceLayers.layer(layerType)


    @pyqtSlot()
    def importData(self):
        """Open the Import dialog for this workspace."""
        if not self.importDialog:
            self.importDialog = ImportDialog(self.iface.mainWindow())
            self.importDialog.setAttribute(Qt.WA_DeleteOnClose)
        self.importDialog.show()


    def findGroup(self):
        """Find this workspace's group in the Layers panel."""
        group = QgsProject.instance().layerTreeRoot().findGroup(self.workspaceName)
        if group is None:
            group = QgsProject.instance().layerTreeRoot().insertGroup(0, self.workspaceName)
        return group


    def addToMap(self, group=None):
        """Add the visible layers of the given type to the QGIS map."""
  
        self.removeFromMap()
        group = group or self.findGroup()
  
        layerStackingOrder = [WaterpointLayer, PipelineLayer, FenceLayer, WateredAreaLayer, LandTypeLayer, DerivedBoundaryLayer, DerivedMetricPaddockLayer, ElevationLayer]
        availableLayers = [l for l in [self.workspaceLayers.layer(layerType) for layerType in layerStackingOrder] if l]
               
        for layer in availableLayers:
            layer.addToMap(group)  
    
    
    def removeFromMap(self):
        """Remove this workspace from the current map view."""
        group = self.findGroup()
        QgsProject.instance().layerTreeRoot().removeChildNode(group)
    

    def setTool(self, tool):
        """Set the current map tool for this workspace."""
        if not isinstance(tool, MapTool):
            raise Glitch(
                f"The {PLUGIN_NAME} tool must be of a recognised type")

        self.unsetTool()
        self.currentTool = tool
        self.iface.mapCanvas().setMapTool(self.currentTool)


    def unsetTool(self):
        """Unset the current map tool for this workspace."""
        if self.currentTool is not None:
            self.currentTool.clear()
            self.currentTool.dispose()
            self.iface.mapCanvas().unsetMapTool(self.currentTool)
            self.currentTool = None


    def setCurrentTimeframe(self, timeframe):
        """Set the current timeframe for this workspace."""
        if self.currentTimeframe != timeframe:
            # If our current feature is not in the new timeframe, deselect it
            if self.selectedFeature and not self.selectedFeature.matchTimeframe(timeframe):
                # qgsDebug("Deselecting feature because it is not in the new timeframe")
                self.deselectFeature()

            self.currentTimeframe = timeframe
            self.currentTimeframeChanged.emit(timeframe)


    def deselectFeature(self):
        """Deselect any currently selected Feature."""
        self.selectedFeaturesChanged.emit([])


    def selectFeature(self, feature):
        """Select a feature."""
        self.selectedFeature = feature
        self.selectedFeaturesChanged.emit([feature])


    @pyqtSlot()
    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        self.unsetTool()

        for viewType, view in self.views.values():
            view.close()
            self.iface.removeDockWidget(view)
            self.onCloseView(viewType)

        self.removeFromMap()
        
        for layerType in self.layerDependencyGraph.unloadOrder():
            self.workspaceLayers.unloadLayer(layerType)
        self.workspaceUnloading.emit()
        

    @pyqtSlot(FeatureLayer, list)
    def onLayerSelectionChanged(self, layer, selection):
        if len(selection) == 1:
            feature = layer.getFeature(selection[0])
            if feature is not None:
                self.selectFeature(feature)


    def openView(self, viewType, dockArea):
        """There is currently ontly one view type, but there may be more in future."""
        if viewType not in self.views:
            view = viewType(self)
            view.setAttribute(Qt.WA_DeleteOnClose)
            view.closingView.connect(lambda: self.onCloseView(viewType))
            self.views[viewType] = view
            self.iface.addDockWidget(dockArea, view)
            view.show()


    @pyqtSlot()
    def openFeatureView(self):
        """Run method that loads and opens the Feature View."""
        self.openView(FeatureView, Qt.BottomDockWidgetArea)


    @pyqtSlot()
    def onCloseView(self, viewType):
        if viewType in self.views:
            del self.views[viewType]
