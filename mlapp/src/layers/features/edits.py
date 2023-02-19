# -*- coding: utf-8 -*-
from contextlib import contextmanager

from qgis.core import QgsVectorLayer

from ...models import Glitch
from ...utils import qgsException, qgsInfo
from ..interfaces import IPersistedFeature, IFeatureLayer


class Edits:

    def __init__(self, upserts=[], deletes=[], layers=[]):
        def _filter(features=[]):
            return [f for f in (features or []) if isinstance(f, IPersistedFeature)]
        self.upserts = _filter(upserts)
        self.deletes = _filter(deletes)
        self.layers = [d for d in (layers or []) if isinstance(d, IFeatureLayer)]

    def editAfter(self, otherEdits=None):
        otherEdits = otherEdits or Edits()
        self.upserts = otherEdits.upserts + self.upserts
        self.deletes = otherEdits.deletes + self.deletes
        self.layers = otherEdits.layers + self.layers
        return self

    def editBefore(self, otherEdits=None):
        otherEdits = otherEdits or Edits()
        self.upserts = self.upserts + otherEdits.upserts
        self.deletes = self.deletes + otherEdits.deletes
        self.layers = self.layers + otherEdits.layers
        return self

    @staticmethod
    def upsert(*features):
        return Edits(upserts=list(features))

    @staticmethod
    def delete(*features):
        return Edits(deletes=list(features))

    @staticmethod
    def notifyLayers(*layers):
        return Edits(layers=list(layers))

    @staticmethod
    @contextmanager
    def editAndCommit(layers):
        try:
            for layer in layers:
                layer.startEditing()
            yield
            for layer in layers:
                layer.commitChanges()
        except Exception as e:
            qgsInfo("Edits.editAndCommit: Exception raised, rolling back edits")
            qgsException()
            for layer in layers:
                layer.rollBack()
            raise e

    @staticmethod
    @contextmanager
    def editAndRollBack(layers):
        layers = set(layers)
        if not all(isinstance(layer, QgsVectorLayer) for layer in layers):
            raise Glitch("When editing layers, all layers must be QgsVectorLayers")
        for layer in layers:
            if layer.isEditable():
                raise Glitch(f"Please end your edit session on {layer.name()} before you run this operation")
        try:
            for layer in layers:
                layer.startEditing()
            yield
            for layer in layers:
                layer.rollBack()
        except Exception as e:
            for layer in layers:
                layer.rollBack()
            raise e
