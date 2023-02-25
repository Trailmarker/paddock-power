# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsTask

from ...utils import JOB_DELAY, PLUGIN_NAME, qgsInfo
from ...models import WorkspaceMixin
from .derive_edits_task import DeriveEditsTask
from .recalculate_features_task import RecalculateFeaturesTask


class AnalyseWorkspaceTask(QgsTask, WorkspaceMixin):

    def __init__(self):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"{PLUGIN_NAME} analuysing the self.workspace …",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)
        
        order = self.workspace.layerDependencyGraph.recalculateOrder()
        recalculateLayers = [self.workspace.workspaceLayers.layer(layerType) for layerType in order]

        self._recalculateTask = RecalculateFeaturesTask(recalculateLayers, self.workspace.onLayerAnalysisComplete)
        self.addSubTask(
            self._recalculateTask,
            dependencies=[],
            subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)

        self._recalculateTask.taskCompleted.connect(self.onRecalculateTaskCompleted)

    def onRecalculateTaskCompleted(self):
        """Called when the recalculate task completes (successfully or otherwise)."""
        order = self.workspace.layerDependencyGraph.deriveOrder()
        deriveLayers = [self.workspace.workspaceLayers.layer(layerType) for layerType in order]
        deriveTask = DeriveEditsTask(deriveLayers, None, self.workspace.onLayerAnalysisComplete)
        self.addSubTask(
            deriveTask,
            dependencies=[self._recalculateTask],
            subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)

    def run(self):
        """Derive features for all layers as specified in subtasks."""
        sleep(JOB_DELAY)
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            qgsInfo(f"{PLUGIN_NAME} failed to fully analyse the '{self.workspaceName}' workspace.")
 