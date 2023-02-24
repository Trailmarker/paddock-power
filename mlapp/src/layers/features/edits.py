# -*- coding: utf-8 -*-
from contextlib import contextmanager

from qgis.core import QgsVectorLayer

from ...models import Glitch, WorkspaceMixin
from ...utils import qgsException, qgsInfo
from ..interfaces import IPersistedFeature, IFeatureLayer


class Edits(WorkspaceMixin):

    def __init__(self, upserts=[], deletes=[]):
        super().__init__()

        def _filter(features=[]):
            return [f for f in (features or []) if isinstance(f, IPersistedFeature)]
        self.upserts = _filter(upserts)
        self.deletes = _filter(deletes)

    def editAfter(self, otherEdits=None):
        otherEdits = otherEdits or Edits()
        self.upserts = otherEdits.upserts + self.upserts
        self.deletes = otherEdits.deletes + self.deletes
        return self

    def editBefore(self, otherEdits=None):
        otherEdits = otherEdits or Edits()
        self.upserts = self.upserts + otherEdits.upserts
        self.deletes = self.deletes + otherEdits.deletes
        return self

    @staticmethod
    def upsert(*features):
        return Edits(upserts=list(features))

    @staticmethod
    def delete(*features):
        return Edits(deletes=list(features))

    @property
    def layers(self):
        return set([f.featureLayer for f in self.upserts + self.deletes])

    def persist(self):
        """Persist these edits to their layers."""
        with Edits.editAndCommit(self.layers):
            for feature in self.upserts:
                feature.upsert()

            for feature in self.deletes:
                feature.delete()

    def notifyPersisted(self):
        """Called when edits are persisted."""
        self.workspace.onPersistEdits(self)

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
