# -*- coding: utf-8 -*-
from ...models import SafeTask
from ..features import Edits


class ChangesetTask(SafeTask):

    def __init__(self, description, editFunction, changeset=None):
        """Input is a correctly ordered batch of layers."""
        self._editFunction = editFunction
        self.changeset = changeset or Edits()
        super().__init__(description)

    def safeRun(self):
        # Same implementation as PersistEditsTask, minus args
        if self.isCanceled():
            return False
        self.edits = self._editFunction() or Edits()
        self.edits.persist()

        self.changeset.editBefore(self.edits)

        return True

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        pass