# -*- coding: utf-8 -*-
from ...models import SafeTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo
from .cleanup_derived_layers_task import CleanupDerivedLayersTask
from .cleanup_layers_task import CleanupLayersTask
from .load_layer_task import LoadLayerTask


class LoadWorkspaceTask(SafeTask):

    def __init__(self, layerDependencyGraph, workspaceLayers, workspaceFile, workspaceName):
        """Input is a Workspace."""

        super().__init__(f"{PLUGIN_NAME} is loading the '{workspaceName}' workspace …")

        loadOrder = layerDependencyGraph.loadOrder()

        # self.safeAddSubTask(CleanupDerivedLayersTask())
        self.safeAddSubTask(CleanupLayersTask(loadOrder))

        for layerType in loadOrder:
            dependentLayerTypes = layerDependencyGraph.getDependencies(layerType)
            self.safeAddSubTask(LoadLayerTask(workspaceLayers, layerType, workspaceFile, dependentLayerTypes))

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to load the workspace.")
