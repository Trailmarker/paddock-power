# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBar, qgsInfo
from ...models import WorkspaceMixin
from ..features import Edits


class DeriveFeaturesMultipleTask(QgsTask, WorkspaceMixin):

    def __init__(self, layers):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"{PLUGIN_NAME} Derive Features Multiple(layers={', '.join([layer.name() for layer in layers])})",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layers = layers
        # self.setDependentLayers([self.layer])

    def run(self):
        """Derive features for a layer."""
        [*head, last] = self.layers
        guiStatusBar(
            f"{PLUGIN_NAME} deriving features for {', '.join([layer.name() for layer in head])} and {last.name()} …")
        readOnlies = [layer.readOnly() for layer in self.layers]

        try:
            for layer in self.layers:
                layer.setReadOnly(False)

            if self.isCanceled():
                return False

            with Edits.editAndCommit(self.layers):
                for layer in self.layers:
                    layer.deriveFeatures(
                        featureProgressCallback=lambda featureCount,
                        total: self.setProgress(
                            featureCount * 100.0 / total),
                        cancelledCallback=self.isCanceled)
                    layer.commitChanges()  # Commit early if we can …
        finally:
            for layer, readOnly in zip(self.layers, readOnlies):
                layer.setReadOnly(readOnly)
        self.setProgress(100.0)
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        self.workspace.onTaskCompleted(self, result)

    def cancel(self):
        qgsInfo(f"QGIS requesting cancellation of {self.description()} for an unknown reason …")
        super().cancel()
