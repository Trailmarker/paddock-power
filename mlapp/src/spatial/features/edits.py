# -*- coding: utf-8 -*-
from contextlib import contextmanager

from qgis.core import QgsVectorLayer

from ...models.glitch import Glitch
from ...utils import qgsInfo


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
    def upsert(*features):
        return Edits(upserts=list(features))

    @staticmethod
    def delete(*features):
        return Edits(deletes=list(features))

    @staticmethod
    @contextmanager
    def editAndCommit(*layers):
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
                layer.commitChanges()
                layer.editsPersisted.emit()
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

    @staticmethod
    def persistEdits(method):
        """Decorator that takes a method returning an Edits object of edits to persist,
        and returns a method that instead persists the edits and returns None."""
        def methodWithPersistEdits(feature, *args, **kwargs):
            edits = method(feature, *args, **kwargs)
            qgsInfo(f"Persisting edits: upserts={repr(edits.upserts)}, deletes={repr(edits.deletes)}")

            layers = set([f.featureLayer for f in edits.upserts + edits.deletes])
            with Edits.editAndCommit(*layers):
                for feature in edits.upserts:
                    feature.upsert()
                for feature in edits.deletes:
                    feature.delete()

            # Signal updates to the rest of the system - TODO?
            for feature in edits.upserts:
                feature.stateChanged.emit(feature)
            for feature in edits.deletes:
                feature.stateChanged.emit(feature)

            return None
        return methodWithPersistEdits
