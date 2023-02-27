# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME, qgsDebug, guiStatusBarAndInfo
from ..interfaces import IPersistedDerivedFeatureLayer
from .changeset_task import ChangesetTask


class DeriveEditsSingleTask(ChangesetTask):

    def __init__(self, layer, changeset):
        """Input is a correctly ordered batch of layers."""
        self.layer = layer
        super().__init__(f"{PLUGIN_NAME} deriving {layer.name()}", self.editFunction, changeset)

    def __repr__(self):
        return f"{type(self).__name__}(layer={self.layer}, changeset={self.changeset})"

    def __str__(self):
        return repr(self)

    def editFunction(self):
        assert isinstance(self.layer, IPersistedDerivedFeatureLayer)
        guiStatusBarAndInfo(self.description())
        return self.layer.deriveFeatures(self.changeset)

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        super().safeFinished(result)
        if result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} derived {self.layer.name()}.")
        else:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to derive {self.layer.name()}.")
