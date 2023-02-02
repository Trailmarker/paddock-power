# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo
from ...models import WorkspaceMixin


class RecalculateFeaturesTask(QgsTask, WorkspaceMixin):

    def __init__(self, layers):
        """Input is a batch of layers (order not important)."""
        super().__init__(
            f"{PLUGIN_NAME} Derive Features(layers={', '.join([layer.name() for layer in layers])})",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layers = layers
        self.obsolete = False

        for layer in self.layers:
            task = RecalculateFeaturesTask(layer)
            self.addSubTask(task, dependencies=[])

    def run(self):
        """Recalculate features for all layers as specified in subtasks."""
        guiStatusBarAndInfo(f"{PLUGIN_NAME} recalculating features complete.")
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
