# -*- coding: utf-8 -*-
from contextlib import contextmanager

from qgis.core import QgsVectorLayer

from ...models.glitch import Glitch
from ...utils import qgsDebug


class Edits:
    def __init__(self, upserts=[], deletes=[]):
        self.upserts = upserts or []
        self.deletes = deletes or []

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
    def upsert(feature):
        return Edits(upserts=[feature])

    @staticmethod
    def delete(feature):
        return Edits(deletes=[feature])

    @staticmethod
    @contextmanager
    def editAndCommit(*layers):
        layers = set(layers)
        if not all(isinstance(layer, QgsVectorLayer) for layer in layers):
            raise Glitch("When editing alayers, all layers must be QgsVectorLayers")
        if any(layer.isEditable() for layer in layers):
            raise Glitch("When editing layers, all layers must initially be in non-editable state")
        try:
            for layer in layers:
                layer.startEditing()
            yield
            for layer in layers:
                layer.commitChanges()
        except Exception as e:
            for layer in layers:
                layer.rollBack()
            raise e

    @staticmethod
    @contextmanager
    def editAndRollBack(*layers):
        layers = set(layers)
        if not all(isinstance(layer, QgsVectorLayer) for layer in layers):
            raise Glitch("When editing alayers, all layers must be QgsVectorLayers")
        if any(layer.isEditable() for layer in layers):
            raise Glitch("When editing layers, all layers must initially be in non-editable state")
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

    @staticmethod
    def persistEdits(method):
        """Decorator that takes a method returning an Edits object of edits to persist,
        and returns a method that instead persists the edits and returns None."""
        def methodWithPersistEdits(feature, *args, **kwargs):
            edits = method(feature, *args, **kwargs)
            qgsDebug(f"Persisting edits: upserts={repr(edits.upserts)}, deletes={repr(edits.deletes)}")

            layers = set([f.featureLayer for f in edits.upserts + edits.deletes])
            with Edits.editAndCommit(*layers):
                for feature in edits.upserts:
                    feature.upsert()
                for feature in edits.deletes:
                    feature.delete()
            return None
        return methodWithPersistEdits
