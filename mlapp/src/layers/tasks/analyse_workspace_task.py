# -*- coding: utf-8 -*-
from ...layers import DerivedBoundaryLayer, DerivedWaterpointBufferLayer, DerivedMetricPaddockLayer, DerivedPaddockLandTypesLayer, DerivedWateredAreaLayer
from ...models import SafeTask, WorkspaceMixin
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo
from .cleanup_layers_task import CleanupLayersTask
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

        # self.safeAddSubTask(DeriveEditsSingleTask(deriveLayers[0], self.changeset))

        for layer in deriveLayers:
            self.safeAddSubTask(DeriveEditsSingleTask(layer, self.changeset))

        self.safeAddSubTask(CleanupLayersTask([
            DerivedBoundaryLayer,
            DerivedWaterpointBufferLayer,
            DerivedMetricPaddockLayer,
            DerivedPaddockLandTypesLayer,
            DerivedWateredAreaLayer], delay=1))

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} analysed the '{self.workspace.workspaceName}' workspace.")
        else:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to analyse the '{self.workspace.workspaceName}' workspace.")
