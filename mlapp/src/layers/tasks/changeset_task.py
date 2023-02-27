# -*- coding: utf-8 -*-
from ..features import Edits, PersistEditsTask


class ChangesetTask(PersistEditsTask):

    def __init__(self, description, editFunction, changeset=None):
        """Input is a correctly ordered batch of layers."""
        self.changeset = changeset or Edits()
        super().__init__(description, editFunction)

    def safeRun(self):
        result = super().safeRun()
        if result:
            # Merge edits into accumulated changeset
            self.changeset.editBefore(self.edits)
        return result

    
