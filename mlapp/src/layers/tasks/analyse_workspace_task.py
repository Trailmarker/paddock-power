# -*- coding: utf-8 -*-
from ...models import SafeTask, WorkspaceMixin
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo
from .cleanup_derived_layers_task import CleanupDerivedLayersTask
from .derive_edits_single_task import DeriveEditsSingleTask
from .recalculate_features_single_task import RecalculateFeaturesSingleTask


class AnalyseWorkspaceTask(SafeTask, WorkspaceMixin):

    def __init__(self):
        """Input is a correctly ordered batch of layers."""
        SafeTask.__init__(self, f"{PLUGIN_NAME} analysing the workspace …")
        WorkspaceMixin.__init__(self)

        self.changeset = None

        recalculateOrder = self.workspace.layerDependencyGraph.recalculateOrder()
        recalculateLayers = [self.workspace.workspaceLayers.layer(layerType) for layerType in recalculateOrder]

        for layer in recalculateLayers:
            self.safeAddSubTask(RecalculateFeaturesSingleTask(layer, self.changeset))

        deriveOrder = self.workspace.layerDependencyGraph.deriveOrder()
        deriveLayers = [self.workspace.workspaceLayers.layer(layerType) for layerType in deriveOrder]

        for layer in deriveLayers:
            self.safeAddSubTask(DeriveEditsSingleTask(layer, self.changeset))

        self.safeAddSubTask(CleanupDerivedLayersTask())

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} analysed the '{self.workspace.workspaceName}' workspace.")
        else:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to analyse the '{self.workspace.workspaceName}' workspace.")
