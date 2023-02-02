# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBar, qgsInfo
from ...models import WorkspaceMixin
from ..features import Edits
from ..interfaces import IPersistedDerivedFeatureLayer


class DeriveFeaturesSingleTask(QgsTask, WorkspaceMixin):

    def __init__(self, layer, onTaskCompleted=None):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"deriving {layer.name()}",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layer = layer
        self.count = 0
        self.total = 0
        self.obsolete = False

        if onTaskCompleted is not None:
            self.taskCompleted.connect(lambda: onTaskCompleted(type(layer), True))

        # self.setDependentLayers([self.layer])

    def run(self):
        """Derive features for a layer."""
        guiStatusBar(f"{PLUGIN_NAME} deriving {self.layer.name()} …")

        # TODO bit of a hack, just trying to reduce contention between these guys
        sleep(0.5)

        assert isinstance(self.layer, IPersistedDerivedFeatureLayer)
        readOnly = self.layer.readOnly()

        try:
            self.layer.setReadOnly(False)

            if self.isCanceled():
                return False

            with Edits.editAndCommit([self.layer]):
                self.layer.deriveFeatures(
                    featureProgressCallback=self.updateCount,
                    cancelledCallback=self.isCanceled)
        finally:
            self.layer.setReadOnly(readOnly)
        self.setProgress(100.0)
        return True

    def updateCount(self, featureCount, total):
        self.count = featureCount
        self.total = total
        self.setProgress((featureCount * 100.0 / total) if total > 0 else 100.0)  # Watch for divzero …

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        self.workspace.onTaskCompleted(self, result, showMessage=False)

    def cancelObsolete(self):
        qgsInfo(f"{PLUGIN_NAME} requesting cancellation of {self.description()} because a newer task has been queued …")
        self.obsolete = True
        super().cancel()

    def cancel(self):
        qgsInfo(f"QGIS requesting cancellation of {self.description()} for an unknown reason …")
        super().cancel()
