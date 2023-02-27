# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo
from .changeset_task import ChangesetTask
from ..interfaces import IPersistedDerivedFeatureLayer, IPersistedFeatureLayer


class RecalculateFeaturesSingleTask(ChangesetTask):

    def __init__(self, layer, changeset=None):
        """Input is a correctly ordered batch of layers."""
        self.layer = layer
        super().__init__(f"{PLUGIN_NAME} recalculating {layer.name()}", self.editFunction, changeset)

    def editFunction(self):
        assert isinstance(self.layer, IPersistedFeatureLayer)
        assert not isinstance(self.layer, IPersistedDerivedFeatureLayer)
        guiStatusBarAndInfo(self.description())
        return self.layer.recalculateFeatures()

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        super().safeFinished(result)
        if result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} recalculated {self.layer.name()}.")
        else:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to recalculate {self.layer.name()} …")
