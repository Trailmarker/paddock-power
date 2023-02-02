# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBar, qgsInfo
from ...models import WorkspaceMixin
from ..features import Edits
from ..interfaces import IPersistedDerivedFeatureLayer, IPersistedFeatureLayer


class RecalculateFeaturesSingleTask(QgsTask, WorkspaceMixin):

    def __init__(self, layer):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"recalculating {layer.name()}",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layer = layer
        self.obsolete = False
        self.count = 0
        self.total = 0

    def run(self):
        """Recalculate features for a layer."""
        guiStatusBar(f"{PLUGIN_NAME} recalculating {self.layer.name()} features …")

        assert isinstance(self.layer, IPersistedFeatureLayer)
        assert not isinstance(self.layer, IPersistedDerivedFeatureLayer)

        readOnly = self.layer.readOnly()

        try:
            self.layer.setReadOnly(False)

            if self.isCanceled():
                return False

            with Edits.editAndCommit([self.layer]):
                self.layer.recalculateFeatures(
                    featureProgressCallback=self.updateCount,
                    cancelledCallback=self.isCanceled)
        finally:
            self.layer.setReadOnly(readOnly)
        self.setProgress(100.0)
        return True
    
    def updateCount(self, featureCount, total):
        self.count = featureCount
        self.total = total
        self.setProgress((featureCount * 100.0 / total) if total > 0 else 100.0) # Watch for divzero …

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
