# -*- coding: utf-8 -*-
from time import sleep

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo
from ...models import WorkspaceMixin


class ProcessFeaturesTask(QgsTask, WorkspaceMixin):

    def __init__(self, getFeatures, processFeatures):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            f"${PLUGIN_NAME} processing features …",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self._getFeatures = getFeatures
        self._processFeatures = processFeatures

    def run(self):
        """Derive features for a layer."""

        self._getFeatures()
        self._processFeatures()

        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} processing features failed …")

    def cancel(self):
        qgsInfo(f"QGIS requesting cancellation of {self.description()} for an unknown reason …")
        super().cancel()
