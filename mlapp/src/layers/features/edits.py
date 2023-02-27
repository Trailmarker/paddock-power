# -*- coding: utf-8 -*-
from contextlib import contextmanager

from qgis.core import QgsVectorLayer

from ...models import Glitch, WorkspaceMixin
from ...utils import ensureIterated, qgsException, qgsInfo
from ..interfaces import IPersistedFeature, IPersistedDerivedFeatureLayer


class Edits(WorkspaceMixin):

    def __init__(self, truncates=[], upserts=[], deletes=[]):
        super().__init__()
        self.truncates = ensureIterated(truncates)
        self.upserts = ensureIterated(upserts)
        self.deletes = ensureIterated(deletes)

        # def _filter(features=[]):
        #     return [f for f in (features or []) if isinstance(f, IPersistedFeature)]

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{type(self).__name__}(truncates={[repr(t) for t in self.truncates]}, upserts={[repr(u) for u in self.upserts]}, deletes={[repr(d) for d in self.deletes]})"

    def __str__(self):
        return repr(self)

    def editAfter(self, otherEdits=None):
        otherEdits = otherEdits or Edits()
        self.truncates = otherEdits.truncates + self.truncates
        self.upserts = otherEdits.upserts + self.upserts
        self.deletes = otherEdits.deletes + self.deletes
        return self

    def editBefore(self, otherEdits=None):
        otherEdits = otherEdits or Edits()
        self.truncates = self.truncates + otherEdits.truncates
        self.upserts = self.upserts + otherEdits.upserts
        self.deletes = self.deletes + otherEdits.deletes
        return self

    @staticmethod
    def truncate(layer):
        return Edits(truncates=[layer])

    @staticmethod
    def upsert(feature):
        return Edits(upserts=[feature])

    @staticmethod
    def delete(feature):
        return Edits(deletes=[feature])

    @property
    def layers(self):
        return set([f.featureLayer for f in (self.upserts + self.deletes)] + self.truncates)

    def layerUpsertFids(self, layer):
        return [f.FID for f in self.upserts if f.featureLayer.id() == layer.id()]

    def layerDeleteFids(self, layer):
        return [f.FID for f in self.deletes if f.featureLayer.id() == layer.id()]

    def layerFids(self, layer):
        fids = self.layerUpsertFids(layer) + self.layerDeleteFids(layer)
        # qgsDebug(f"Edits.layerFids({layer}): fids: {fids}")
        return fids

    def persist(self):
        """Persist these edits to their layers."""
        with Edits.editAndCommit(self.layers):
            for layer in self.truncates:
                if not isinstance(layer, IPersistedDerivedFeatureLayer):
                    raise Glitch(
                        f"Cannot truncate layer {layer.name()} because it is not an IPersistedDerivedFeatureLayer")
                layer.dataProvider().truncate()

            for feature in self.deletes:
                feature.delete()

            for feature in self.upserts:
                feature.upsert()
        
            # Return a response … 
            return self

    def notifyPersisted(self):
        """Called when edits are persisted."""
        self.workspace.onPersistEdits(self)

    @staticmethod
    @contextmanager
    def editAndCommit(layers):
        readOnlies = [(layer, layer.readOnly()) for layer in layers]
        try:
            for layer in layers:
                layer.setReadOnly(False)
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
        finally:
            # Restore previous read only status if necessary
            for layer, readOnly in readOnlies:
                layer.setReadOnly(readOnly)
                

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
