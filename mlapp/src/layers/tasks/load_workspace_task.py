# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsTask

from ...utils import JOB_DELAY, PLUGIN_NAME, guiStatusBarAndInfo
from .load_layer_task import LoadLayerTask


class LoadWorkspaceTask(QgsTask):

    def __init__(self, layerDependencyGraph, workspaceLayers, workspaceFile, workspaceName):
        """Input is a Workspace."""

        super().__init__(
            f"{PLUGIN_NAME} is loading the '{workspaceName}' workspace …",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self._layerDependencyGraph = layerDependencyGraph
        self._workspaceLayers = workspaceLayers
        self._workspaceFile = workspaceFile
        self._workspaceName = workspaceName
        
        self.configure()
    
    def configure(self):
        loadOrder = self._layerDependencyGraph.loadOrder()

        predecessors = []
        for layerType in loadOrder:
            dependentLayerTypes = self._layerDependencyGraph.getDependencies(layerType)
            task = LoadLayerTask(self._workspaceLayers, layerType, self._workspaceFile, dependentLayerTypes)
            task.taskTerminated.connect(self.cancel)

            self.addSubTask(
                task, dependencies=predecessors,
                subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
            predecessors.append(task)
    
    def run(self):
        f"""Load all layers in a {PLUGIN_NAME} workspace."""
        sleep(JOB_DELAY)
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to load the '{self._workspaceName}' workspace.")
