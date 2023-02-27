# -*- coding: utf-8 -*-
from os.path import basename

from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot

from qgis.core import QgsApplication, QgsProject

from ..layers.fields import Timeframe
from ..layers.tasks import AnalyseWorkspaceTask, DeriveEditsTask, LoadWorkspaceTask
from ..layers import (BoundaryLayer, PaddockLayer,
                      ElevationLayer, FenceLayer, LandTypeLayer,
                      PipelineLayer, WateredAreaLayer, WaterpointLayer)
from ..tools.map_tool import MapTool
from ..utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo
from .glitch import Glitch
from .layer_dependency_graph import LayerDependencyGraph
from .workspace_layers import WorkspaceLayers

# Initialize Qt resources from file resources.py
from ...resources_rc import *


class Workspace(QObject):
    # emit this signal when a selected PersistedFeature is updated
    featureLayerSelected = pyqtSignal(str)
    featureLayerDeselected = pyqtSignal(str)
    timeframeChanged = pyqtSignal(Timeframe)
    workspaceLoaded = pyqtSignal()

    def __init__(self, iface, workspaceFile):

        self.ready = False

        super().__init__(iface.mainWindow())

        self.loadWorkspaceTask = None
        self.loadWorkspaceTaskId = -1
        self._deriveEditsTask = None
        self._deriveFeaturesTaskId = -1
        self._analyseWorkspaceTask = None
        self._analyseWorkspaceTaskId = -1

        self.selectedFeatures = {}

        self.iface = iface
        self.workspaceFile = workspaceFile
        self.workspaceName = basename(workspaceFile)

        self.currentTool = None
        self.timeframe = Timeframe.Future

        self.timeframeChanged.connect(self.deselectLayers)

        # Load workspace
        self.layerDependencyGraph = LayerDependencyGraph()
        self.workspaceLayers = WorkspaceLayers()

        self.loadWorkspaceTask = LoadWorkspaceTask(
            self.layerDependencyGraph,
            self.workspaceLayers,
            self.workspaceFile,
            self.workspaceName)
        self.loadWorkspaceTask.taskCompleted.connect(self.onWorkspaceLoaded)
        self.loadWorkspaceTaskId = QgsApplication.taskManager().addTask(self.loadWorkspaceTask)

    def onWorkspaceLoaded(self):
        qgsInfo(f"Workspace.onWorkspaceLoaded()")

        # Wiring some stuff for selected features …
        self.workspaceLayers.addLayersToWorkspace(self)
        self.workspaceLoaded.emit()

        self.addToMap()
     

    def findGroup(self):
        """Find this workspace's group in the Layers panel."""
        group = QgsProject.instance().layerTreeRoot().findGroup(PLUGIN_NAME)
        if group is None:
            group = QgsProject.instance().layerTreeRoot().insertGroup(0, PLUGIN_NAME)
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

    def deselectLayers(self, selectedLayerId=None):
        """Deselect any currently selected Feature."""
        for layerId in [l for l in self.selectedFeatures.keys() if l != selectedLayerId]:
            # qgsInfo(f"Workspace.deselectLayers({layerType.__name__})")
            del self.selectedFeatures[layerId]
            self.featureLayerDeselected.emit(layerId)

    def selectFeature(self, feature):
        """Select a feature."""
        # qgsInfo(f"Workspace.selectFeature({feature})")
        selectedLayerId = feature.featureLayer.id()
        # qgsInfo(f"Workspace.selectFeature({feature}): selectedLayerId={selectedLayerId}")
        self.selectedFeatures[selectedLayerId] = feature

        # If we are going to focus on the new feature, deselect the old layers
        if feature.featureLayer.focusOnSelect():
            qgsInfo(f"Workspace.selectFeature({feature}): focusOnSelect, deselecting other layers")
            self.deselectLayers(selectedLayerId)

        # Select on the new layer either way
        self.featureLayerSelected.emit(selectedLayerId)
        # qgsInfo(f"Workspace.featureLayerSelected.emit({selectedLayerId})")

    def selectedFeature(self, layerId):
        """Return the selected feature for the given layer type."""
        return self.selectedFeatures[layerId] if layerId in self.selectedFeatures else None

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

    def deriveEdits(self, changeset):
        """Winnow and re-analyse a batch of updated layers."""
        deriveEditsTask = QgsApplication.taskManager().task(self._deriveFeaturesTaskId)
        if deriveEditsTask and deriveEditsTask.isActive():
            deriveEditsTask.cancel()
            self._deriveFeaturesTaskId = -1

        order = self.layerDependencyGraph.deriveOrder(type(layer) for layer in changeset.layers)
        layers = [self.workspaceLayers.layer(layerType) for layerType in order]
        self._deriveEditsTask = DeriveEditsTask(layers, changeset)
        self._deriveFeaturesTaskId = QgsApplication.taskManager().addTask(self._deriveEditsTask)

    def analyseWorkspace(self):
        """Winnow and re-analyse a batch of updated layers."""
        analyseWorkspaceTask = QgsApplication.taskManager().task(self._analyseWorkspaceTaskId)
        if analyseWorkspaceTask and analyseWorkspaceTask.isActive():
            analyseWorkspaceTask.cancel()
            self._deriveFeaturesTaskId = -1

        self._analyseWorkspaceTask = AnalyseWorkspaceTask()
        self._analyseWorkspaceTaskId = QgsApplication.taskManager().addTask(self._analyseWorkspaceTask)

  
