# -*- coding: utf-8 -*-
from qgis.core import QgsApplication

from ...models import SafeTask
from ...utils import PLUGIN_NAME, qgsDebug, qgsInfo
from .edits import Edits


class PersistEditsTask(SafeTask):

    def __init__(self, description, editFunction, *args, **kwargs):
        """Input is a closure over a FeatureAction handler for a given Feature."""
        super().__init__(description)

        self.edits = None
        self._editFunction = editFunction
        self._args = args
        self._kwargs = kwargs

    def safeRun(self):
        """Carry out a function that generates Feature edit operations, and persist the edits."""
        if self.isCanceled():
            return False
        self.edits = self._editFunction(*self._args, **self._kwargs) or Edits()
        self.edits.persist()
        return True

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        pass


def persistEdits(editFunction, *args, **kwargs):
    """Utility function to queue an action returning edits to a PersistEditsTask."""
    qgsDebug(f"persistEdits({editFunction}, {args}, {kwargs})")
    currentTask = PersistEditsTask(f"{PLUGIN_NAME} saving your data …", editFunction, *args, **kwargs)
    QgsApplication.taskManager().addTask(currentTask)
