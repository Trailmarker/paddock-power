# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo


class LoadWorkspaceLayerTask(QgsTask):

    def __init__(self, layerType, workspaceFile):
        f"""Input is a layerType that must implement ILayer, and a {PLUGIN_NAME} workspace GeoPackage file."""
        super().__init__(
            f"{PLUGIN_NAME} LoadWorkspaceLayer(layerType={layerType.__name__}, workspaceFile={workspaceFile})",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.layerTYpe = layerType
        self.workspaceFile = workspaceFile

    def run(self):
        f"""Load a layer of the nominated type in a {PLUGIN_NAME} workspace."""
        raise NotImplementedError

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        self.workspace.onTaskCompleted(self, result)

    def cancel(self):
        super().cancel()
