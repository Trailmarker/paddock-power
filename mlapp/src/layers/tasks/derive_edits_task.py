# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsTask

from ...models import WorkspaceMixin
from ...utils import JOB_DELAY, PLUGIN_NAME, guiStatusBarAndInfo
from .derive_edits_single_task import DeriveEditsSingleTask


class DeriveEditsTask(QgsTask, WorkspaceMixin):

    def __init__(self, layers, edits=None, onTaskCompleted=None):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"deriving features for {len(layers)} layers",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layers = layers
        self.edits = edits
        # self.setDependentLayers([self.layers])

        predecessors = []
        for layer in self.layers:
            task = DeriveEditsSingleTask(layer, self.edits, onTaskCompleted=onTaskCompleted)
            task.taskTerminated.connect(self.cancel)

            self.addSubTask(
                task, dependencies=predecessors,
                subTaskDependency=QgsTask.SubTaskDependency.ParentDependsOnSubTask)
            predecessors.append(task)

    def run(self):
        """Derive features for all layers as specified in subtasks."""
        sleep(JOB_DELAY)
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to fully derive the '{self.workspaceName}' workspace.")
