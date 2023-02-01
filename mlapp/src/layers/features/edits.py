# -*- coding: utf-8 -*-
from contextlib import contextmanager

from qgis.core import QgsVectorLayer

from ...models import Glitch
from ...utils import qgsInfo
from . import IPersistedFeature


class Edits:

    def __init__(self, upserts=[], deletes=[]):
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

    @staticmethod
    def persistFeatures(function):
        """Decorator that takes a method returning an Edits object of edits to persist,
        and returns a method that instead persists the edits and returns None."""
        def callableWithPersistFeatures(*args, **kwargs):
            # Get the result of the inner function
            edits = function(*args, **kwargs)
            qgsInfo(f"Edits.persistFeatures: upserts={repr(edits.upserts)}, deletes={repr(edits.deletes)}")

            layers = set([f.featureLayer for f in edits.upserts + edits.deletes])

            with Edits.editAndCommit(layers):
                for feature in edits.upserts:
                    # feature.recalculate()
                    feature.upsert()
                for feature in edits.deletes:
                    feature.delete()

        return callableWithPersistFeatures

    @staticmethod
    def analyseLayers(layers):
        """Input is a correctly ordered batch of layers."""
        readOnlies = [(layer, layer.readOnly()) for layer in layers]
        try:
            for layer in layers:
                layer.setReadOnly(False)

            for layer in layers:
                with Edits.editAndCommit([layer]):
                    layer.analyseFeatures()
        finally:
            for (layer, readOnly) in readOnlies:
                layer.setReadOnly(readOnly)
                layer.triggerRepaint()
