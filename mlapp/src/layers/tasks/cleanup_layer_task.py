# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsProject

from ...models import SafeTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo


class CleanupLayerTask(SafeTask):

    def __init__(self, layerId, delay=5):
        """Input is a correctly ordered batch of layers."""
        super().__init__(f"{PLUGIN_NAME} cleaning up layer {layerId} …")
        self.layerId = layerId
        self.delay = delay

    def safeRun(self):
        """Derive features for a layer."""
        # Sleep a configurable amount
        sleep(self.delay)

        guiStatusBarAndInfo(f"{PLUGIN_NAME} Cleaning up {self.layerId} …")
        QgsProject.instance().removeMapLayer(self.layerId)

        return True

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to clean up layer {self.layerId} …")
