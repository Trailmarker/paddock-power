# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo
from ...models import WorkspaceMixin
from .derive_features_single_task import DeriveFeaturesSingleTask


class DeriveFeaturesTask(QgsTask, WorkspaceMixin):

    def __init__(self, layers):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"{PLUGIN_NAME} Derive Features(layers={', '.join([layer.name() for layer in layers])})",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layers = layers
        self.obsolete = False
        # self.setDependentLayers([self.layers])

        predecessor = None
        for layer in self.layers:
            task = DeriveFeaturesSingleTask(layer)
            if predecessor:
                self.addSubTask(
                    task, dependencies=[predecessor],
                    subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
            else:
                self.addSubTask(
                    task, dependencies=[],
                    subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
            predecessor = task

    def run(self):
        """Derive features for all layers as specified in subtasks."""
        guiStatusBarAndInfo(f"{PLUGIN_NAME} deriving features complete.")
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        self.workspace.onTaskCompleted(self, result)

    def cancelObsolete(self):
        qgsInfo(f"{PLUGIN_NAME} requesting cancellation of {self.description()} because a newer task has been queued.")
        self.obsolete = True
        super().cancel()

    def cancel(self):
        qgsInfo(f"{PLUGIN_NAME} requesting cancellation of {self.description()} for an unknown reason.")
        super().cancel()
