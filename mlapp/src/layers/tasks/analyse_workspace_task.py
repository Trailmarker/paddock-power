# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, qgsInfo
from ...models import WorkspaceMixin
from .derive_features_task import DeriveFeaturesTask
from .recalculate_features_task import RecalculateFeaturesTask


class AnalyseWorkspaceTask(QgsTask, WorkspaceMixin):

    def __init__(self):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"workspace analysis",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.obsolete = False
        workspace = self.workspace # WorkspaceMixin

        order = workspace.layerDependencyGraph.recalculateOrder()
        recalculateLayers = [workspace.workspaceLayers.layer(layerType) for layerType in order]

        recalculateTask = RecalculateFeaturesTask(recalculateLayers, workspace.onLayerAnalysisComplete)
        self.addSubTask(
            recalculateTask,
            dependencies=[],
            subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
        
        order = workspace.layerDependencyGraph.deriveOrder()
        deriveLayers = [workspace.workspaceLayers.layer(layerType) for layerType in order]
        deriveTask = DeriveFeaturesTask(deriveLayers, workspace.onLayerAnalysisComplete)
        self.addSubTask(
            deriveTask,
            dependencies=[recalculateTask],
            subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)

    def run(self):
        """Derive features for all layers as specified in subtasks."""
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        self.workspace.onTaskCompleted(self, result)

    def cancelObsolete(self):
        qgsInfo(f"{PLUGIN_NAME} cancelling task: '{self.description()}' because a newer task has been queued.")
        self.obsolete = True
        super().cancel()

    def cancel(self):
        qgsInfo(f"QGIS cancelling task: '{self.description()}' eg due to quitting or user intervention.")
        super().cancel()
