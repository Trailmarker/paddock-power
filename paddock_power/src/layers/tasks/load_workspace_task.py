# -*- coding: utf-8 -*-
from ...layers import PipelineLayer
from ...models import WorkspaceTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsException


class LoadWorkspaceTask(WorkspaceTask):

    def __init__(self, workspace):
        """Input is a Workspace."""
        super().__init__(f"{PLUGIN_NAME} is loading the '{workspace.workspaceName}' workspace …", workspace)

    def safeRun(self):
        try:
            loadOrder = self.workspace.layerDependencyGraph.loadOrder()

            for layerType in loadOrder:
                if self.isCanceled():
                    return False
                dependentLayerTypes = self.workspace.layerDependencyGraph.getDependencies(layerType)
                dependentLayers = [self.workspace.workspaceLayers.layer(dependentLayerType)
                                   for dependentLayerType in dependentLayerTypes]

                layer = layerType(self.workspace.workspaceFile, *dependentLayers)
                self.workspace.workspaceLayers.addLayer(layerType, layer)

                guiStatusBarAndInfo(f"{PLUGIN_NAME} {layer.name()} loaded.")

            guiStatusBarAndInfo(f"{PLUGIN_NAME} loaded the '{self.workspace.workspaceName}' workspace.")
            return True

        except Exception:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to load workspace.")
            qgsException()
            return False

    def safeFinished(self, _):
        """Called when task completes (successfully or otherwise)."""
        for layer in self.workspace.workspaceLayers.layers():
            layer.connectWorkspace(self.workspace)
