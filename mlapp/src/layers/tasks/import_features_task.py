# -*- coding: utf-8 -*-
from ...models import WorkspaceTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsException


class ImportFeaturesTask(WorkspaceTask):

    def __init__(self, workspace, importableLayer, importLayer, fieldMap):
        """Input is a closure over a FeatureAction handler for a given Feature."""
        WorkspaceTask.__init__(self, f"{PLUGIN_NAME} impporting features …", workspace)

        self.importableLayer = importableLayer
        self.importLayer = importLayer
        self.fieldMap = fieldMap

    def safeRun(self):
        """Generate Feature edit operations from an import, and persist the edits."""
        try:
            if self.isCanceled():
                return False

            edits = self.importableLayer.importFeatures(self.importLayer, self.fieldMap, self.raiseIfCancelled)
            edits.persist(raiseErrorIfTaskHasBeenCancelled=self.raiseIfCancelled)

        except Exception as e:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to import features.")
            qgsException()
            return False

        guiStatusBarAndInfo(f"{PLUGIN_NAME} imported features.")
        return True

    def safeFinished(self, _):
        """Called when task completes (successfully or otherwise)."""
        pass
