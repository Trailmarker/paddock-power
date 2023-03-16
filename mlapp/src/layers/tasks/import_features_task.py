# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME, guiStatusBarAndInfo
from ..interfaces import IImportableFeatureLayer


class ImportFeaturesTask(PersistEditsTask):

    def __init__(self, layer, importLayer, fieldMap):
        """Input is a correctly ordered batch of layers."""
        self.layer = layer
        self.importLayer = importLayer
        self.fieldMap = fieldMap

        super().__init__(f"{PLUGIN_NAME} importing {layer.name()}", True, self.editFunction)

    def editFunction(self):
        assert isinstance(self.layer, IImportableFeatureLayer)
        guiStatusBarAndInfo(f"{PLUGIN_NAME} importing {self.importLayer.name()} to {self.layer.name()} …")

        return self.layer.importFeatures(self.importLayer, self.fieldMap)

    def safeFinished(self, result):
        """Called when task completes (successfully or otherwise)."""
        super().safeFinished(result)
        if not result:
            guiStatusBarAndInfo(f"{PLUGIN_NAME} failed to import {self.importLayer.name()} to {self.layer.name()} …")
