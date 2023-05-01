# -*- coding: utf-8 -*-
from ...models import WorkspaceTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsException
from ..interfaces import IPersistedDerivedFeatureLayer, IPersistedFeatureLayer


class AnalyseWorkspaceTask(WorkspaceTask):

    def __init__(self, workspace):
        """Input is a batch of layers (order not important)."""
        WorkspaceTask.__init__(self, f"{PLUGIN_NAME} analysing the workspace …", workspace)

    def safeRun(self):
        """Input is a correctly ordered batch of layers."""
        try:
            recalculateOrder = self.workspace.layerDependencyGraph.recalculateOrder()
            recalculateLayers = [self.workspace.workspaceLayers.layer(layerType) for layerType in recalculateOrder]
            recalculateLayerNames = ", ".join(layer.name() for layer in recalculateLayers)
            guiStatusBarAndInfo(f"{PLUGIN_NAME} recalculating {recalculateLayerNames}")

            for layer in recalculateLayers:
                assert isinstance(layer, IPersistedFeatureLayer)
                assert not isinstance(layer, IPersistedDerivedFeatureLayer)

                if self.isCanceled():
                    return False
                recalculatedEdits = layer.recalculateFeatures(raiseErrorIfTaskHasBeenCancelled=self.raiseIfCancelled)
                if self.isCanceled():
                    return False
                recalculatedEdits.persist(raiseErrorIfTaskHasBeenCancelled=self.raiseIfCancelled)
                if self.isCanceled():
                    return False

                layer.editsPersisted.emit()
                guiStatusBarAndInfo(f"{PLUGIN_NAME} recalculated {layer.name()}.")

            deriveOrder = self.workspace.layerDependencyGraph.deriveOrder()
            deriveLayers = [self.workspace.workspaceLayers.layer(layerType) for layerType in deriveOrder]
            deriveLayerNames = ", ".join(layer.name() for layer in deriveLayers)
            guiStatusBarAndInfo(f"{PLUGIN_NAME} deriving {deriveLayerNames}")

            for layer in deriveLayers:
                if self.isCanceled():
                    return False
                derivedEdits = layer.deriveFeatures(
                    changeset=None, raiseErrorIfTaskHasBeenCancelled=self.raiseIfCancelled)
                if self.isCanceled():
                    return False
                derivedEdits.persist(raiseErrorIfTaskHasBeenCancelled=self.raiseIfCancelled)
                if self.isCanceled():
                    return False

                layer.editsPersisted.emit()
                guiStatusBarAndInfo(f"{PLUGIN_NAME} derived {layer.name()}.")

            guiStatusBarAndInfo(f"{PLUGIN_NAME} analysed the '{self.workspace.workspaceName}' workspace.")
            return True

        except Exception:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to analyse the '{self.workspace.workspaceName}' workspace.")
            qgsException()
            return False

    def safeFinished(self, _):
        """Called when task completes (successfully or otherwise)."""
        pass
