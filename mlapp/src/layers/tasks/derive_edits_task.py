# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import qgsInfo
from ...models import WorkspaceMixin
from .derive_features_single_task import DeriveEditsSingleTask


class DeriveEditsTask(QgsTask, WorkspaceMixin):

    def __init__(self, layers, edits=None, onTaskCompleted=None):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"deriving features for {len(layers)} layers",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layers = layers
        self.edits = edits
        # self.setDependentLayers([self.layers])

        predecessor = None
        for layer in self.layers:
            task = DeriveEditsSingleTask(layer, self.edits, onTaskCompleted=onTaskCompleted)
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
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        # self.workspace.onTaskCompleted(self, result)

    # def makesObsolete(self, otherTask):
    #     """Return true if this task makes the other task obsolete."""
    #     if isinstance(otherTask, DeriveEditsTask):
    #         layers = set([layer.id() for layer in self.layers])
    #         otherLayers = set([layer.id() for layer in otherTask.layers])
    #         return len(layers.intersection(otherLayers)) > 0
    #     return False

    def cancel(self):
        qgsInfo(f"QGIS cancelling task: '{self.description()}' eg due to quitting or user intervention.")
        super().cancel()
