# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot

from qgis.core import QgsProject

from ..layers.edits import Edits
from ..layers import (LandTypeConditionTable, DerivedBoundaryLayer, DerivedMetricPaddockLayer,
                      DerivedPaddockLandTypesLayer, DerivedWateredAreaLayer, DerivedWaterpointBufferLayer,
                      ElevationLayer, FenceLayer, LandTypeLayer, PaddockLandTypesLayer, PaddockLayer,
                      PipelineLayer, WateredAreaLayer, WaterpointBufferLayer, WaterpointLayer)
from ..layers.fields import Timeframe
from ..tools.map_tool import MapTool
from ..utils import PLUGIN_NAME, guiStatusBar, qgsInfo, qgsDebug
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

    def __init__(self, plugin, iface, workspaceFile):

        self.ready = False

        super().__init__(iface.mainWindow())

        self.workspaceName = PLUGIN_NAME

        self.iface = iface
        self.workspaceFile = workspaceFile

        qgsDebug(f"{PLUGIN_NAME} initialising layers …")
        self.landTypeLayer = LandTypeLayer(self.workspaceFile)
        guiStatusBar(f"{PLUGIN_NAME} {self.landTypeLayer.name()} loaded …")
        self.conditionTable = LandTypeConditionTable(self.workspaceFile)
        guiStatusBar(f"{PLUGIN_NAME} {self.conditionTable.name()} loaded …")
        self.elevationLayer = ElevationLayer(
            self.workspaceFile)
        guiStatusBar(f"{PLUGIN_NAME} {self.elevationLayer.name()} loaded …")
        self.paddockLayer = PaddockLayer(
            self.workspaceFile,
            self.conditionTable)
        guiStatusBar(f"{PLUGIN_NAME} {self.paddockLayer.name()} loaded …")
        self.waterpointLayer = WaterpointLayer(
            self.workspaceFile,
            self.elevationLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.waterpointLayer.name()} loaded …")
        self.derivedWaterpointBufferLayer = DerivedWaterpointBufferLayer(
            self.paddockLayer,
            self.waterpointLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.derivedWaterpointBufferLayer.name()} loaded …")
        self.waterpointBufferLayer = WaterpointBufferLayer(
            self.workspaceFile,
            self.derivedWaterpointBufferLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.waterpointBufferLayer.name()} loaded …")
        self.derivedWateredAreaLayer = DerivedWateredAreaLayer(
            self.paddockLayer,
            self.waterpointBufferLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.derivedWateredAreaLayer.name()} loaded …")
        self.wateredAreaLayer = WateredAreaLayer(
            self.workspaceFile,
            self.derivedWateredAreaLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.wateredAreaLayer.name()} loaded …")
        self.derivedPaddockLandTypesLayer = DerivedPaddockLandTypesLayer(
            self.conditionTable,
            self.paddockLayer,
            self.landTypeLayer,
            self.wateredAreaLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.derivedPaddockLandTypesLayer.name()} loaded …")
        self.paddockLandTypesLayer = PaddockLandTypesLayer(
            self.workspaceFile,
            self.derivedPaddockLandTypesLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.paddockLandTypesLayer.name()} loaded …")
        self.derivedMetricPaddockLayer = DerivedMetricPaddockLayer(
            self.paddockLayer,
            self.paddockLandTypesLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.derivedMetricPaddockLayer.name()} loaded …")
        self.fenceLayer = FenceLayer(
            self.workspaceFile)
        guiStatusBar(f"{PLUGIN_NAME} {self.elevationLayer.name()} loaded …")
        self.pipelineLayer = PipelineLayer(
            self.workspaceFile)
        guiStatusBar(f"{PLUGIN_NAME} {self.pipelineLayer.name()} loaded …")
        self.derivedBoundaryLayer = DerivedBoundaryLayer(
            self.paddockLayer)
        guiStatusBar(f"{PLUGIN_NAME} {self.derivedBoundaryLayer.name()} loaded …")
        self.workspaceLayers = WorkspaceLayers(
            *[self.landTypeLayer,
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
              self.derivedBoundaryLayer])

        self.layerDependencyGraph = LayerDependencyGraph()

        self.currentTool = None
        self.timeframe = Timeframe.Current

        self.timeframeChanged.connect(self.deselectLayers)

        qgsInfo(f"{PLUGIN_NAME} analysis layers initialised …")

        # Wiring some stuff for selected features …
        self.__selectedFeatures = {}

        self.addToMap()

        qgsInfo(f"{PLUGIN_NAME} workspace load complete")

        self.ready = True

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
        if isinstance(timeframe, str):
            timeframe = Timeframe[timeframe]

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
