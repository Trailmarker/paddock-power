# -*- coding: utf-8 -
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsException
from .save_edits_task import SaveEditsTask


class SaveEditsAndDeriveTask(SaveEditsTask):

    def __init__(self, description, workspace, editFunction, *args, **kwargs):
        """Input is a closure over a FeatureAction handler for a given Feature."""
        super().__init__(description, workspace, editFunction, *args, **kwargs)

    def safeRun(self):
        """Carry out a function that generates Feature edit operations, and persist the edits."""
        saveEditsResult = super().safeRun()

        if not saveEditsResult:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to save and derive downstream features …")
            return False

        try:
            # Analyse dependency
            if self.isCanceled():
                return False

            changeset = self.edits
            order = self.workspace.layerDependencyGraph.deriveOrder(type(layer) for layer in changeset.layers)
            layers = [self.workspace.workspaceLayers.layer(layerType) for layerType in order]

            for i, layer in enumerate(layers):
                guiStatusBarAndInfo(f"{PLUGIN_NAME} deriving {layer.name()} ({i + 1} of {len(layers)}) …")
                if self.isCanceled():
                    return False
                derivedEdits = layer.deriveFeatures(changeset, raiseErrorIfTaskHasBeenCancelled=self.raiseIfCancelled)
                if self.isCanceled():
                    return False
                derivedEdits.persist(raiseErrorIfTaskHasBeenCancelled=self.raiseIfCancelled)
                if self.isCanceled():
                    return False

                changeset.editBefore(derivedEdits)
                layer.editsPersisted.emit()
                guiStatusBarAndInfo(f"{PLUGIN_NAME} derived {layer.name()}.")

            guiStatusBarAndInfo(f"{PLUGIN_NAME} derived all features.")
            return True

        except Exception as e:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to derive some features.")
            qgsException()
            return False

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        pass
