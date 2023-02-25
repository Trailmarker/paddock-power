# -*- coding: utf-8 -*-
import os

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo, qgsDebug
from .load_layer_task import LoadLayerTask


class LoadWorkspaceTask(QgsTask):

    def __init__(self, layerDependencyGraph, workspaceLayers, workspaceFile, workspaceName):
        """Input is a Workspace."""
        
        super().__init__(
            f"{PLUGIN_NAME} is loading the '{workspaceName}' workspace …",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.workspaceFile = workspaceFile
        self.workspaceName = workspaceName
        loadOrder = layerDependencyGraph.loadOrder()
                
        predecessors = []
        for layerType in loadOrder:
            dependentLayerTypes = layerDependencyGraph.getDependencies(layerType)
            task = LoadLayerTask(workspaceLayers, layerType, workspaceFile, dependentLayerTypes)
            task.taskTerminated.connect(self.cancel)
          
            self.addSubTask(
                task, dependencies=predecessors,
                subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
            predecessors.append(task)
            
    def run(self):
        f"""Load all layers in a {PLUGIN_NAME} workspace."""
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        qgsInfo(f"LoadWorkspaceTask.finished()")

    def cancel(self):
        super().cancel()
