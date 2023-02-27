# -*- coding: utf-8 -*-
from time import sleep

from ...models import SafeTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo
from ..interfaces import IMapLayer


class CleanupLayersTask(SafeTask):

    def __init__(self, layerTypes, delay=0):
        """Input is a correctly ordered batch of layers."""
        super().__init__(f"{PLUGIN_NAME} cleaning up layers …")
        self.layerTypes = layerTypes
        self.delay = delay

    def safeRun(self):
        """Derive features for a layer."""
        # Sleep a configurable amount
        sleep(self.delay)

        for layerType in self.layerTypes:
            if issubclass(layerType, IMapLayer):
                layerType.detectAndRemoveAllOfType()

        return True

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to clean up layers …")
