# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import qgsInfo
from ...models import WorkspaceMixin
from .recalculate_features_single_task import RecalculateFeaturesSingleTask


class RecalculateFeaturesTask(QgsTask, WorkspaceMixin):

    def __init__(self, layers, onTaskCompleted=None):
        """Input is a batch of layers (order not important)."""
        super().__init__(
            f"Recalculating features for {len(layers)} layers",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layers = layers

        for layer in self.layers:
            task = RecalculateFeaturesSingleTask(layer)
            if onTaskCompleted:
                task.taskCompleted.connect(lambda: onTaskCompleted(type(layer), True))
                task.taskTerminated.connect(lambda: onTaskCompleted(type(layer), False))
            self.addSubTask(task, dependencies=[])

    def run(self):
        """Recalculate features for all layers as specified in subtasks."""
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        pass

    def cancel(self):
        qgsInfo(f"QGIS cancelling task: '{self.description()}' eg due to quitting or user intervention.")
        super().cancel()
