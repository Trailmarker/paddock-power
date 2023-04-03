# -*- coding: utf-8 -*-
from .. import ElevationLayer
from ...models import WorkspaceTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsException


class ImportElevationLayerTask(WorkspaceTask):

    def __init__(self, workspace, importLayer):
        """Input is a raster layer containing elevation data to be imported to the workspace."""
        WorkspaceTask.__init__(self, f"{PLUGIN_NAME} importing elevation data …", workspace)

        self.workspace = workspace
        self.importLayer = importLayer

    def safeRun(self):
        """Import elevation data to a workspace, overwriting existing elevation data."""
        try:
            if self.isCanceled():
                return False

            # Runs gdal:translate under the hood via the processing engine
            ElevationLayer.importToStore(self.workspace.workspaceFile, self.importLayer)

        except Exception:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to import elevation data.")
            qgsException()
            return False

        guiStatusBarAndInfo(f"{PLUGIN_NAME} imported elevation data.")
        return True

    def safeFinished(self, _):
        """Called when task completes (successfully or otherwise)."""
        pass
