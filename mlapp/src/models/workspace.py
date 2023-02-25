# -*- coding: utf-8 -*-
from os.path import basename

from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot

from qgis.core import QgsApplication, QgsProject, QgsTask

from ..layers.fields import Timeframe
from ..layers.interfaces import IFeatureLayer
from ..layers.tasks import AnalyseWorkspaceTask, DeriveEditsTask, LoadWorkspaceTask, RecalculateFeaturesTask
from ..layers import (LandTypeConditionTable, BoundaryLayer, PaddockLayer,
                      ElevationLayer, FenceLayer, LandTypeLayer, PaddockLandTypesLayer, BasePaddockLayer,
                      PipelineLayer, WateredAreaLayer, WaterpointBufferLayer, WaterpointLayer)
from ..tools.map_tool import MapTool
from ..utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo, qgsDebug
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
    workspaceLoaded = pyqtSignal()

    def __init__(self, iface, workspaceFile):

        self.ready = False

        super().__init__(iface.mainWindow())

        # These handles are needed to stop QGIS aggressively cleaning up QgsTask objects
        self._loadWorkspaceTask = None
        self._deriveFeaturesTask = None
        self._recalculateFeaturesTask = None
        
        self.__selectedFeatures = {}

        self.workspaceName = PLUGIN_NAME
        self.iface = iface
        self.workspaceFile = workspaceFile
        self.workspaceName = basename(workspaceFile)
        
        self.currentTool = None
        self.timeframe = Timeframe.Future

        self.timeframeChanged.connect(self.deselectLayers)
        
        # Load workspace
        self.layerDependencyGraph = LayerDependencyGraph()
        self.workspaceLayers = WorkspaceLayers()

        self._loadWorkspaceTask = LoadWorkspaceTask(self.layerDependencyGraph, self.workspaceLayers, self.workspaceFile, self.workspaceName)
        self._loadWorkspaceTask.taskCompleted.connect(self.onWorkspaceLoaded)
        QgsApplication.taskManager().addTask(self._loadWorkspaceTask)

    def onWorkspaceLoaded(self):
        qgsInfo(f"Workspace.onWorkspaceLoaded()")
        
        # Wiring some stuff for selected features …
        self.addToMap()
        # Set some convenience variables as usual
        self.workspaceLayers.setWorkspaceLayerAttributes(self)
        self.workspaceLoaded.emit()

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
            BoundaryLayer,
            PaddockLayer,
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
            # qgsInfo(f"Workspace.deselectLayers({layerType.__name__})")
            del self.__selectedFeatures[layerType]
            self.featureLayerDeselected.emit(layerType)

    def selectFeature(self, feature):
        """Select a feature."""
        # qgsInfo(f"Workspace.selectFeature({feature})")
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
            cleanupByName(cls.defaultName())

        for layerType in self.layerDependencyGraph.unloadOrder():
            self.workspaceLayers.unloadLayer(layerType)

    def onLayerLoaded(self, layer):
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {layer.name()} loaded …")

    def onTaskCompleted(self, task, result, showMessage=True):
        if showMessage:
            if result:
                guiStatusBarAndInfo(f"{PLUGIN_NAME} {task.description()} succeeded.")
            else:
                guiStatusBarAndInfo(
                    f"{PLUGIN_NAME} {task.description()} failed for an unknown reason. You may want to check the {PLUGIN_NAME}, 'Python Error' and other log messages for any exception details.")

    def deriveEdits(self, edits):
        """Winnow and re-analyse a batch of updated layers."""        
        order = self.layerDependencyGraph.deriveOrder(type(layer) for layer in edits.layers)
        layers = [self.workspaceLayers.layer(layerType) for layerType in order]

        self._deriveFeaturesTask = DeriveEditsTask(layers, edits, self.onLayerAnalysisComplete)
        QgsApplication.taskManager().addTask(self._deriveFeaturesTask)
        return self._deriveFeaturesTask

    def recalculateLayers(self):
        """Winnow and re-analyse a batch of updated layers."""

        self._recalculateFeaturesTask = AnalyseWorkspaceTask()
        QgsApplication.taskManager().addTask(self._recalculateFeaturesTask)

    def onLayerAnalysisComplete(self, layerType, result):
        """Handle a completed recalculation of a layer."""
        if result:
            layer = self.workspaceLayers.layer(layerType)
            qgsDebug(f"{type(self).__name__}.onLayerAnalysisComplete: {type(layer).__name__}.featuresChanged.emit()")
            layer.featuresChanged.emit()

    def onPersistEdits(self, edits):
        """Handle a change to the features of one or more layer."""

        # Emit a signal to any layer subscribers that these features have changedinstance
        for layer in edits.layers:
            layer.featuresChanged.emit()

        # Re-derive other features that depend on these features
        self.deriveEdits(edits)
