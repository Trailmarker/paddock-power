# -*- coding: utf-8 -*-
from ...models import SafeTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsException
from ..features import Edits


class SaveEditsTask(SafeTask):

    def __init__(self, description, workspace, editFunction, *args, **kwargs):
        """Input is a closure over a FeatureAction handler for a given Feature."""
        super().__init__(description)

        self.workspace = workspace
        self.editFunction = editFunction
        self.args = args
        self.kwargs = kwargs

        self.edits = None

    def safeRun(self):
        """Carry out a function that generates Feature edit operations, and persist the edits."""
        try:
            # Persist original edits
            if self.isCanceled():
                return False
            self.edits = self.editFunction(*self.args, **self.kwargs) or Edits()
            self.edits.persist(RAISE_IF_CANCELLED=self.raiseIfCancelled)

        except Exception as e:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to save edits.")
            qgsException()
            return False

        guiStatusBarAndInfo(f"{PLUGIN_NAME} saved edits.")
        return True

    def safeFinished(self, _):
        """Called when task completes (successfully or otherwise)."""
        pass
