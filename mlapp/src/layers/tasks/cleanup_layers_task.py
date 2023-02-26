# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...layers import DerivedBoundaryLayer, DerivedWaterpointBufferLayer, DerivedMetricPaddockLayer, DerivedPaddockLandTypesLayer, DerivedWateredAreaLayer
from ...models import SafeTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo
from ..interfaces import IDerivedFeatureLayer


class CleanupLayersTask(SafeTask):

    def __init__(self):
        """Input is a correctly ordered batch of layers."""
        super().__init__(f"{PLUGIN_NAME} cleaning up all derived layers …")

    def safeRun(self):
        """Derive features for a layer."""

        mapLayers = QgsProject.instance().mapLayers().values()
        layerTypes = [
            DerivedBoundaryLayer,
            DerivedWaterpointBufferLayer,
            DerivedMetricPaddockLayer,
            DerivedPaddockLandTypesLayer,
            DerivedWateredAreaLayer]

        for layerType in layerTypes:
            if issubclass(layerType, IDerivedFeatureLayer):
                layerType.detectAndRemoveAllOfType()

        return True

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to clean up layers …")
