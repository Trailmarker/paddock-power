# -*- coding: utf-8 -*-
from ...models import SafeTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo
from .recalculate_features_single_task import RecalculateFeaturesSingleTask


class RecalculateFeaturesTask(SafeTask):

    def __init__(self, layers):
        """Input is a batch of layers (order not important)."""
        super().__init__(f"{PLUGIN_NAME} recalculating features for {len(layers)} layers")

        self.layers = layers
        allLayerNames = ", ".join(layer.name() for layer in self.layers)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} recalculating {allLayerNames}")

        for layer in self.layers:
            self.safeAddSubTask(RecalculateFeaturesSingleTask(layer))

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(
                f"{PLUGIN_NAME} failed to recalculate features for {len(self.layers)} layers.")
