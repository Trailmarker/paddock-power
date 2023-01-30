# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, Qt, pyqtSignal, pyqtSlot

from qgis.core import QgsProject

from ..spatial.features.edits import Edits
from ..spatial.layers.condition_table import ConditionTable
from ..spatial.layers.derived_boundary_layer import DerivedBoundaryLayer
from ..spatial.layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from ..spatial.layers.derived_paddock_land_types_layer import DerivedPaddockLandTypesLayer
from ..spatial.layers.derived_watered_area_layer import DerivedWateredAreaLayer
from ..spatial.layers.derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.feature_layer import FeatureLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.land_type_layer import LandTypeLayer
from ..spatial.layers.paddock_land_types_layer import PaddockLandTypesLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.watered_area_layer import WateredAreaLayer
from ..spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer
from ..spatial.fields.timeframe import Timeframe
from ..tools.map_tool import MapTool
from ..utils import PLUGIN_NAME, qgsInfo
from ..views.feature_view.feature_view import FeatureView
from ..widgets.import_dialog.import_dialog import ImportDialog
from .glitch import Glitch
from .layer_dependency_graph import LayerDependencyGraph
from .workspace_layers import WorkspaceLayers

# Initialize Qt resources from file resources.py
from ...resources_rc import *


class Workspace(QObject):
    # emit this signal when a selected PersistedFeature is updated
    featureLayerSelected = pyqtSignal(type)
    featureLayerDeselected = pyqtSignal(type)
    timeframeChanged = pyqtSignal(Timeframe)
    featuresChanged = pyqtSignal(list)

    def __init__(self,
                 iface,
                 workspaceFile: str,
                 workspaceLayers: WorkspaceLayers):

        self.ready = False

        super().__init__(iface.mainWindow())

        self.workspaceName = PLUGIN_NAME

        self.workspaceFile = workspaceFile
        self.workspaceLayers = workspaceLayers
        self.layerDependencyGraph = LayerDependencyGraph()

        self.iface = iface
        self.currentTool = None
        self.timeframe = Timeframe.Current
        self.view = None
        self.importDialog = None

        self.timeframeChanged.connect(self.deselectLayers)
        # self.featuresChanged.connect(self.updateLayers)

        # For convenient reference
        self.landTypeLayer = self.workspaceLayers.layer(LandTypeLayer)
        self.conditionTable = self.workspaceLayers.layer(ConditionTable)
        self.paddockLayer = self.workspaceLayers.layer(PaddockLayer)
        self.elevationLayer = self.workspaceLayers.layer(ElevationLayer)
        self.waterpointLayer = self.workspaceLayers.layer(WaterpointLayer)
        self.derivedWaterpointBufferLayer = self.workspaceLayers.layer(DerivedWaterpointBufferLayer)
        self.waterpointBufferLayer = self.workspaceLayers.layer(WaterpointBufferLayer)
        self.derivedWateredAreaLayer = self.workspaceLayers.layer(DerivedWateredAreaLayer)
        self.wateredAreaLayer = self.workspaceLayers.layer(WateredAreaLayer)
        self.derivedPaddockLandTypesLayer = self.workspaceLayers.layer(DerivedPaddockLandTypesLayer)
        self.paddockLandTypesLayer = self.workspaceLayers.layer(PaddockLandTypesLayer)
        self.derivedMetricPaddockLayer = self.workspaceLayers.layer(DerivedMetricPaddockLayer)
        self.fenceLayer = self.workspaceLayers.layer(FenceLayer)
        self.pipelineLayer = self.workspaceLayers.layer(PipelineLayer)
        self.derivedBoundarylayer = self.workspaceLayers.layer(DerivedBoundaryLayer)

        qgsInfo(f"{PLUGIN_NAME} analysis layers initialised …")

        # Wiring some stuff for selected features …
        self.__selectedFeatures = {}
 
        qgsInfo(f"{PLUGIN_NAME} workspace connected …")

        self.addToMap()

        qgsInfo(f"{PLUGIN_NAME} load complete.")

        self.ready = True

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

        layerStackingOrder = [
            WaterpointLayer,
            PipelineLayer,
            FenceLayer,
            WateredAreaLayer,
            LandTypeLayer,
            DerivedBoundaryLayer,
            DerivedMetricPaddockLayer,
            ElevationLayer]
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

    def setTimeframe(self, timeframe):
        """Set the current timeframe for this workspace."""
        if self.timeframe != timeframe:
            self.timeframe = timeframe
            self.timeframeChanged.emit(timeframe)

    def deselectLayers(self, selectedLayerType=None):
        """Deselect any currently selected Feature."""
        for layerType in [l for l in self.__selectedFeatures.keys() if l != selectedLayerType]:
            qgsInfo(f"Workspace.deselectLayers({layerType.__name__})")
            del self.__selectedFeatures[layerType]
            self.featureLayerDeselected.emit(layerType)

    def selectFeature(self, feature):
        """Select a feature."""
        qgsInfo(f"Workspace.selectFeature({feature})")
        selectedLayerType = type(feature.featureLayer)
        self.__selectedFeatures[selectedLayerType] = feature

        # If we are going to focus on the new feature, deselect the old layers
        if selectedLayerType.focusOnSelect():
            self.deselectLayers(selectedLayerType)

        # Select on the new layer either way
        self.featureLayerSelected.emit(selectedLayerType)

    def selectedFeature(self, layerType):
        """Return the selected feature for the given layer type."""
        return self.__selectedFeatures[layerType] if layerType in self.__selectedFeatures else None

    @pyqtSlot()
    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        self.unsetTool()

        if self.view:
            self.view.close()
            self.iface.removeDockWidget(self.view)

        self.removeFromMap()
        
        def cleanupByName(name):
            f"""Remove all layers from the current project with the given names."""
            for layer in QgsProject.instance().mapLayers().values():
                if layer.name() == name:
                    QgsProject.instance().removeMapLayers([layer.id()])
        
        for cls in self.layerDependencyGraph.unloadOrder():
            cleanupByName(cls.NAME)

        for layerType in self.layerDependencyGraph.unloadOrder():
            self.workspaceLayers.unloadLayer(layerType)

    @pyqtSlot()
    def openFeatureView(self):
        """Run method that loads and opens the Feature View."""
        if self.view is None:
            self.view = FeatureView()
            self.view.setAttribute(Qt.WA_DeleteOnClose)
            self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.view)
            self.view.show()

    def analysisOrder(self):
        """Return the order in which layers should be analsed."""
        order = self.layerDependencyGraph.analysisOrder()
        return [self.workspaceLayers.layer(layerType) for layerType in order]
    
    def updateOrder(self, updatedLayers):
        """Return the order in which layers should be updated."""
        updateOrder = self.layerDependencyGraph.updateOrder(updatedLayers)
        return [self.workspaceLayers.layer(layerType) for layerType in updateOrder]

    
    def updateLayers(self, updatedLayers):
        """Winnow and re-analyse a batch of updated layers."""
        updateOrder = self.updateOrder(updatedLayers)
        qgsInfo(f"{PLUGIN_NAME} deriving layers … {updateOrder}")
        Edits.analyseLayers(updateOrder)
        qgsInfo(f"{PLUGIN_NAME} load complete.")
   
   
    def analyseLayers(self):
        """Winnow and re-analyse a batch of updated layers."""        
        analysisOrder = self.analysisOrder()
        qgsInfo(f"{PLUGIN_NAME} analysing layers …")
        Edits.analyseLayers(analysisOrder)
        qgsInfo(f"{PLUGIN_NAME} load complete.")
