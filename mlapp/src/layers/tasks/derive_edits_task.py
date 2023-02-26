# -*- coding: utf-8 -*-
from ...models import SafeTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo
from .derive_edits_single_task import DeriveEditsSingleTask


class DeriveEditsTask(SafeTask):

    def __init__(self, layers, changeset=None):
        """Input is a correctly ordered batch of layers."""
        super().__init__(f"{PLUGIN_NAME} deriving features for {len(layers)} layers")

        self.layers = layers
        allLayerNames = ", ".join(layer.name() for layer in self.layers)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} deriving {allLayerNames}")

        self.changeset = changeset  # Note—this is shared between all subtasks

        for layer in self.layers:
            self.safeAddSubTask(DeriveEditsSingleTask(layer, self.changeset))

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(
                f"{PLUGIN_NAME} failed to derive features for {len(self.layers)} layers.")
