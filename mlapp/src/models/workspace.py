# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot

from qgis.core import QgsApplication, QgsProject, QgsTask

from ..layers.fields import Timeframe
from ..layers.interfaces import IFeatureLayer
from ..layers.tasks import AnalyseWorkspaceTask, DeriveFeaturesTask, RecalculateFeaturesTask
from ..layers import (LandTypeConditionTable, BoundaryLayer, MetricPaddockLayer,
                      ElevationLayer, FenceLayer, LandTypeLayer, PaddockLandTypesLayer, PaddockLayer,
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

    def __init__(self, iface, workspaceFile):

        self.ready = False

        super().__init__(iface.mainWindow())

        self.workspaceName = PLUGIN_NAME
        self.iface = iface
        self.workspaceFile = workspaceFile

        self._deriveFeaturesTask = None
        self._recalculateFeaturesTask = None

        self.layerDependencyGraph = LayerDependencyGraph()

        self.currentTool = None
        self.timeframe = Timeframe.Current

        self.timeframeChanged.connect(self.deselectLayers)

        self.landTypeLayer = LandTypeLayer(self.workspaceFile)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.landTypeLayer.name()} loaded …")
        self.conditionTable = LandTypeConditionTable(self.workspaceFile)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.conditionTable.name()} loaded …")
        self.elevationLayer = ElevationLayer(
            self.workspaceFile)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.elevationLayer.name()} loaded …")
        self.paddockLayer = PaddockLayer(
            self.workspaceFile,
            self.conditionTable)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.paddockLayer.name()} loaded …")
        self.waterpointLayer = WaterpointLayer(
            self.workspaceFile,
            self.elevationLayer)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.waterpointLayer.name()} loaded …")
        self.waterpointBufferLayer = WaterpointBufferLayer(
            self.workspaceFile,
            self.paddockLayer,
            self.waterpointLayer)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.waterpointBufferLayer.name()} loaded …")
        self.wateredAreaLayer = WateredAreaLayer(
            self.workspaceFile,
            self.paddockLayer,
            self.waterpointBufferLayer)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.wateredAreaLayer.name()} loaded …")
        self.paddockLandTypesLayer = PaddockLandTypesLayer(
            self.workspaceFile,
            self.conditionTable,
            self.paddockLayer,
            self.landTypeLayer,
            self.wateredAreaLayer)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.paddockLandTypesLayer.name()} loaded …")
        self.metricPaddockLayer = MetricPaddockLayer(
            self.workspaceFile,
            self.paddockLayer,
            self.paddockLandTypesLayer)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.metricPaddockLayer.name()} loaded …")
        self.fenceLayer = FenceLayer(
            self.workspaceFile)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.fenceLayer.name()} loaded …")
        self.pipelineLayer = PipelineLayer(
            self.workspaceFile)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.pipelineLayer.name()} loaded …")
        self.boundaryLayer = BoundaryLayer(
            self.workspaceFile,
            self.paddockLayer)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} {self.boundaryLayer.name()} loaded …")
        self.workspaceLayers = WorkspaceLayers(
            *[self.landTypeLayer,
              self.conditionTable,
              self.paddockLayer,
              self.elevationLayer,
              self.waterpointLayer,
              self.waterpointBufferLayer,
              self.wateredAreaLayer,
              self.paddockLandTypesLayer,
              self.metricPaddockLayer,
              self.fenceLayer,
              self.pipelineLayer,
              self.boundaryLayer])

        qgsInfo(f"{PLUGIN_NAME} feature layers initialised …")

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
            BoundaryLayer,
            MetricPaddockLayer,
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

    def onTaskCompleted(self, task, result, showMessage=True):
        if showMessage:
            if result:
                guiStatusBarAndInfo(f"{PLUGIN_NAME} {task.description()} succeeded.")
            if not result and task.obsolete:
                guiStatusBarAndInfo(f"{PLUGIN_NAME} {task.description()} was marked obsolete.")
            if not result and not task.obsolete:
                guiStatusBarAndInfo(
                    f"{PLUGIN_NAME} {task.description()} failed for an unknown reason. You may want to check the {PLUGIN_NAME}, 'Python Error' and other log messages for any exception details.")

    def deriveLayers(self, updatedLayerTypes=None):
        """Winnow and re-analyse a batch of updated layers."""
        order = self.layerDependencyGraph.deriveOrder(updatedLayerTypes)
        layers = [self.workspaceLayers.layer(layerType) for layerType in order]

        self._deriveFeaturesTask = DeriveFeaturesTask(layers, self.onLayerAnalysisComplete)
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

    def onFeaturesPersisted(self, layerTypes):
        """Handle a change to the features of one or more layer."""
        featureLayerTypes = [layerType for layerType in layerTypes if issubclass(layerType, IFeatureLayer)]

        # Emit a signal to any layer subscribers that these features have changedinstance
        for layerType in featureLayerTypes:
            qgsDebug(f"{type(self).__name__}.onFeaturesPersisted: {layerType.__name__}.featuresChanged.emit()")
            self.workspaceLayers.layer(layerType).featuresChanged.emit()

        # Re-derive other features that depend on these features
        self.deriveLayers(featureLayerTypes)
