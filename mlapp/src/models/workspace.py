# -*- coding: utf-8 -*-
from os.path import basename

from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot

from qgis.core import QgsProject, QgsSnappingConfig

from ..layers.fields import Timeframe
from ..layers.tasks import AnalyseWorkspaceTask, SaveEditsAndDeriveTask, LoadWorkspaceTask
from ..utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo
from ..widgets.tools.map_tool import MapTool
from .glitch import Glitch
from .layer_dependency_graph import LayerDependencyGraph
from .task_handle import TaskHandle
from .workspace_layers import WorkspaceLayers

# Initialize Qt resources from file resources.py
from ...resources_rc import *


class Workspace(QObject):
    # emit this signal when a selected PersistedFeature is updated
    featureLayerSelected = pyqtSignal(str)
    lockChanged = pyqtSignal(bool)
    timeframeChanged = pyqtSignal(Timeframe)
    workspaceLoaded = pyqtSignal()

    def __init__(self, iface, workspaceFile):

        super().__init__(iface.mainWindow())

        self._locked = False

        self.loadWorkspaceTask = TaskHandle(LoadWorkspaceTask, self)
        self.loadWorkspaceTask.taskCompleted.connect(self.onLoadWorkspaceTaskCompleted)

        self.analyseWorkspaceTask = TaskHandle(AnalyseWorkspaceTask, self)
        self.analyseWorkspaceTask.taskCompleted.connect(self.onAnalyseWorkspaceTaskCompleted)
        self.saveEditsTask = TaskHandle(SaveEditsAndDeriveTask, self)

        self.selectedFeatures = {}

        self.iface = iface
        self.workspaceFile = workspaceFile
        self.workspaceName = basename(workspaceFile)

        self.currentTool = None
        self.timeframe = Timeframe.Future

        self.timeframeChanged.connect(self.deselectLayers)

        self.layerDependencyGraph = LayerDependencyGraph()
        self.workspaceLayers = WorkspaceLayers()

        # Clean up all layers
        cleanupIds = [layerId for layerType in self.layerDependencyGraph.cleanupOrder()
                      for layerId in layerType.detectAllOfType(workspaceFile)]
        QgsProject.instance().removeMapLayers(cleanupIds)

        for layerType in self.layerDependencyGraph.cleanupOrder():
            layerType.removeAllOfType(workspaceFile)

        # Load workspace async
        self.loadWorkspace()

    def locked(self):
        """Return True if the workspace is locked."""
        return self._locked

    def lock(self):
        """Lock the workspace."""
        self._locked = True
        self.lockChanged.emit(True)

    def unlock(self):
        """Unlock the workspace."""
        self._locked = False
        self.lockChanged.emit(False)

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

        displayOrder = self.layerDependencyGraph.displayOrder()
        availableLayers = [l for l in [self.workspaceLayers.layer(layerType) for layerType in displayOrder] if l]

        for layer in availableLayers:
            layer.addToMap(group)

    def removeFromMap(self):
        """Remove this workspace from the current map view."""
        group = self.findGroup()
        QgsProject.instance().layerTreeRoot().removeChildNode(group)

    def setTool(self, tool):
        """Set the current map tool for this workspace."""
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
            qgsInfo(f"Workspace.deselectLayers({selectedLayerId}")
            layer = QgsProject.instance().mapLayer(layerId)
            layer.removeSelection()
            del self.selectedFeatures[layerId]

    def selectFeature(self, feature):
        """Select a feature."""
        selectedLayerId = feature.featureLayer.id()
        self.selectedFeatures[selectedLayerId] = feature

        # If we are going to focus on the new feature, deselect the old layers
        if feature.focusOnSelect():
            qgsInfo(f"Workspace.selectFeature({feature}): focusOnSelect, deselecting other layers")
            self.deselectLayers(selectedLayerId)

        # This is kinda legacy now
        self.featureLayerSelected.emit(selectedLayerId)

    def selectedFeature(self, layerId):
        """Return the selected feature for the given layer type."""
        return self.selectedFeatures[layerId] if layerId in self.selectedFeatures else None

    @pyqtSlot()
    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        self.unsetTool()
        self.removeFromMap()

    def mapLayer(self, layerId):
        if layerId == self.landTypeConditionTable.id():
            return self.landTypeConditionTable
        else:
            return QgsProject.instance().mapLayer(layerId)

    def onLayerLoaded(self, layer):
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {layer.name()} loaded …")

    def onTaskCompleted(self, task, result, showMessage=True):
        if showMessage:
            if result:
                guiStatusBarAndInfo(f"{PLUGIN_NAME} {task.description()} succeeded.")
            else:
                guiStatusBarAndInfo(
                    f"{PLUGIN_NAME} {task.description()} failed for an unknown reason. You may want to check the {PLUGIN_NAME}, 'Python Error' and other log messages for any exception details.")

    def loadWorkspace(self):
        self.loadWorkspaceTask.run(self)

    def onLoadWorkspaceTaskCompleted(self):
        self.workspaceLayers.addLayersToWorkspace(self)
        self.addToMap()

        # TODO this is a bit of a bizarre hack. Without this line, our project
        # ends up loaded with corrupt snapping configuration (from a QGIS 3 bug, perhaps)
        # that causes QGIS to crash instead of saving the project file.
        QgsProject.instance().setSnappingConfig(QgsSnappingConfig())

        self.workspaceLoaded.emit()

    def analyseWorkspace(self):
        """Winnow and re-analyse a batch of updated layers."""
        self.analyseWorkspaceTask.run(self)

    def onAnalyseWorkspaceTaskCompleted(self):
        """Clean up all the derived layers."""
        pass

    def saveEditsAndDerive(self, editFunction, *args, **kwargs):
        """Persist this feature and also queue up all required derivation."""

        self.saveEditsTask.run(
            f"{PLUGIN_NAME} saving edits and deriving changes …",
            self,
            editFunction, *args, **kwargs
        )
