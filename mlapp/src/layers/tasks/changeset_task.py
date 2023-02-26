# -*- coding: utf-8 -*-
from ..features import Edits, PersistEditsTask


class ChangesetTask(PersistEditsTask):

    def __init__(self, description, editFunction, changeset=None):
        """Input is a correctly ordered batch of layers."""
        self.changeset = changeset or Edits()
        super().__init__(description, editFunction)

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        super().safeFinished(result)
        if result:
            # Merge edits into accumulated changeset
            self.changeset.editBefore(self.edits)
