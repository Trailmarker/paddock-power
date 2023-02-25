# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsTask

from ...utils import JOB_DELAY, PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo
from ...models import WorkspaceMixin
from ..features import Edits
from ..interfaces import IPersistedDerivedFeatureLayer


class DeriveEditsSingleTask(QgsTask, WorkspaceMixin):

    def __init__(self, layer, edits, onTaskCompleted=None):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"deriving {layer.name()}",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self._layer = layer
        self._edits = edits
        self._count = 0
        self._total = 0

        if onTaskCompleted is not None:
            self.taskCompleted.connect(lambda: onTaskCompleted(type(layer), True))

    def run(self):
        """Derive features for a layer."""
        guiStatusBarAndInfo(f"{PLUGIN_NAME} deriving {self._layer.name()} …")

        assert isinstance(self._layer, IPersistedDerivedFeatureLayer)
        readOnly = self._layer.readOnly()

        try:
            self._layer.setReadOnly(False)

            if self.isCanceled():
                return False

            with Edits.editAndCommit([self._layer]):
                self._layer.deriveFeatures(self._edits,
                    featureProgressCallback=self.updateCount,
                    cancelledCallback=self.isCanceled)
        finally:
            self._layer.setReadOnly(readOnly)
        self.setProgress(100.0)
        sleep(JOB_DELAY)
        return True

    def updateCount(self, featureCount, total):
        self._count = featureCount
        self._total = total
        self.setProgress((featureCount * 100.0 / total) if total > 0 else 100.0)  # Watch for divzero …

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to derive {self._layer.name()} …")

