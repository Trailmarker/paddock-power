# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest

from .. import BasePaddockLayer
from ...models import WorkspaceTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsException


class ImportFeatureLayerTask(WorkspaceTask):

    def __init__(self, workspace, targetLayer, importLayer, fieldMap):
        """Input is a target layer in the workspace (Base Paddocks, Waterpoints, etc), and a layer
           to import features from, together with a mapping of fields between the two layers."""
        WorkspaceTask.__init__(self, f"{PLUGIN_NAME} importing features …", workspace)

        self.workspace = workspace
        self.targetLayer = targetLayer
        self.importLayer = importLayer
        self.fieldMap = fieldMap

    def safeRun(self):
        """Generate Feature edit operations from an import, and persist the edits."""
        try:
            if self.isCanceled():
                return False

            notImportingPaddocks = not isinstance(self.targetLayer, BasePaddockLayer)

            if notImportingPaddocks and not self.workspace.hasBasePaddocks:
                # guiWarning(f"{PLUGIN_NAME} you must import {BasePaddockLayer.defaultName()} before all other property data.")
                guiStatusBarAndInfo(
                    f"{PLUGIN_NAME} abandoned import because there are no {BasePaddockLayer.defaultName()}.")
                return False

            # Constrain imported features to the neighbourhood of the Property's Base Paddocks
            importFeatureRequest = QgsFeatureRequest().setFilterRect(self.workspace.basePaddockLayer.neighbourhood) if notImportingPaddocks else None

            edits = self.targetLayer.importFeatures(self.importLayer, self.fieldMap, importFilter=importFeatureRequest, raiseIfCancelled=self.raiseIfCancelled)
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
