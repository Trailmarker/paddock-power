# -*- coding: utf-8 -*-

from qgis.core import QgsApplication, QgsTask

from ...utils import qgsInfo
from .edits import Edits


class PersistEditsTask(QgsTask):

    def __init__(self, editFunction, *args, **kwargs):
        """Input is a closure over a FeatureAction handler for a given Feature."""
        super().__init__(
            f"PersistEditsTask",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)  # | QgsTask.Hidden) TODO not available in 3.22

        self._edits = None
        self._editFunction = editFunction
        self._args = args
        self._kwargs = kwargs

    def run(self):
        """Carry out a function that generates Feature edit operations, and persist the edits."""

        self._edits = self._editFunction(*self._args, **self._kwargs) or Edits()
        self._edits.persist()

        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if result:
            self._edits.notifyPersisted()

    def cancel(self):
        qgsInfo(f"QGIS cancelling task: '{self.description()}' eg due to quitting or user intervention.")
        super().cancel()


def persistEdits(feature, editFunction, *args, **kwargs):
    """Utility function to queue an action returning edits to a PersistEditsTask."""
    feature.currentTask = PersistEditsTask(editFunction, feature, *args, **kwargs)
    QgsApplication.taskManager().addTask(feature.currentTask)
