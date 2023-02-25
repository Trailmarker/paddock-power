# -*- coding: utf-8 -*-
from qgis.core import QgsTask

from ...models import Glitch
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsDebug, qgsError


class LoadLayerTask(QgsTask):

    def __init__(self, workspaceLayers, layerType, workspaceFile, dependentLayerTypes):
        f"""Input is a layerType that must implement ILayer, and the arguments to construct it."""
        super().__init__(
            f"{PLUGIN_NAME} load {layerType.defaultName()} …",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self._layer = None
        self._workspaceLayers = workspaceLayers
        self._layerType = layerType
        self._workspaceFile = workspaceFile
        self._dependentLayerTypes = dependentLayerTypes

    def run(self):
        f"""Load a layer of the nominated type in a {PLUGIN_NAME} workspace."""
        dependentLayers = [self._workspaceLayers.layer(dependentLayerType)
                           for dependentLayerType in self._dependentLayerTypes]
        # qgsDebug(
        #     f"LoadLayerTask.run(): self._layerType={self._layerType.__name__}, self._workspaceFile={self._workspaceFile}, dependentLayers={dependentLayers}")

        self._layer = self._layerType(self._workspaceFile, *dependentLayers)
        return True

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        if result:
            self._workspaceLayers.addLayer(self._layerType, self._layer)
            guiStatusBarAndInfo(f"{PLUGIN_NAME} {self._layer.name()} loaded.")
        else:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} error loading {self._layerType.defaultName()}")

    def cancel(self):
        super().cancel()
