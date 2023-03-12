# -*- coding: utf-8 -*-
from time import sleep

from ...models import SafeTask
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsException
from ..interfaces import IPersistedDerivedFeatureLayer, IPersistedFeatureLayer


class AnalyseWorkspaceTask(SafeTask):

    def __init__(self, workspace):
        """Input is a batch of layers (order not important)."""
        SafeTask.__init__(self, f"{PLUGIN_NAME} analysing the workspace …")

        self.workspace = workspace

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
                recalculatedEdits = layer.recalculateFeatures()
                if self.isCanceled():
                    return False
                recalculatedEdits.persist()
                if self.isCanceled():
                    return False

                layer.editsPersisted.emit()
                guiStatusBarAndInfo(f"{PLUGIN_NAME} recalculated {layer.name()}.")
                sleep(self.TASK_DELAY)

            deriveOrder = self.workspace.layerDependencyGraph.deriveOrder()
            deriveLayers = [self.workspace.workspaceLayers.layer(layerType) for layerType in deriveOrder]
            deriveLayerNames = ", ".join(layer.name() for layer in deriveLayers)
            guiStatusBarAndInfo(f"{PLUGIN_NAME} deriving {deriveLayerNames}")

            for layer in deriveLayers:
                if self.isCanceled():
                    return False
                derivedEdits = layer.deriveFeatures()
                if self.isCanceled():
                    return False
                derivedEdits.persist()
                if self.isCanceled():
                    return False

                layer.editsPersisted.emit()
                guiStatusBarAndInfo(f"{PLUGIN_NAME} derived {layer.name()}.")
                sleep(self.TASK_DELAY)

            guiStatusBarAndInfo(f"{PLUGIN_NAME} analysed the '{self.workspace.workspaceName}' workspace.")
            return True

        except Exception:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to analyse the '{self.workspace.workspaceName}' workspace.")
            qgsException()
            return False

    def safeFinished(self, _):
        """Called when task completes (successfully or otherwise)."""
        pass
