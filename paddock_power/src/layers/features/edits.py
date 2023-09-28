# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractproperty
from collections import defaultdict
from contextlib import contextmanager

from qgis.core import QgsVectorLayer

from ...models import Glitch, WorkspaceMixin
from ...utils import qgsException, qgsInfo
from .land_type_condition import LandTypeCondition


class Edits(WorkspaceMixin):
    @classmethod
    def sort(cls, edits):
        return sorted(edits, key=lambda edit: edit.order)

    class Edit(ABC):
        @abstractmethod
        def persist(self):
            pass

        @abstractproperty
        def layer(self):
            pass

        def sameLayer(self, layer):
            return self.layer.id() == layer.id()

    class Truncate(Edit):
        def __init__(self, layer):
            super().__init__()
            self.order = 1
            self._layer = layer

        def __repr__(self):
            """Return a string representation of the Edit."""
            return f"{type(self).__name__}(layer={self.layer.id()})"

        def __str__(self):
            return repr(self)

        def persist(self):
            self.layer.dataProvider().truncate()

        @property
        def layer(self):
            return self._layer

    class BulkAdd(Edit):
        def __init__(self, layer, features):
            super().__init__()
            self.order = 2
            self._layer = layer
            self.features = features

        def __repr__(self):
            """Return a string representation of the Edit."""
            return f"{type(self).__name__}(layer={self.layer.id()}, len(features)={len(self.features)})"

        def __str__(self):
            return repr(self)

        def persist(self):
            self.layer.dataProvider().addFeatures(self.features)

        @property
        def layer(self):
            return self._layer

    class Upsert(Edit):
        def __init__(self, feature):
            super().__init__()
            self.order = 3
            self.feature = feature

        def __repr__(self):
            """Return a string representation of the Edit."""
            return f"{type(self).__name__}(feature={self.feature})"

        def __str__(self):
            return repr(self)

        def persist(self):
            self.feature.upsert()

        @property
        def layer(self):
            return self.feature.featureLayer

    class UpsertTable(Edit):
        def __init__(self, feature):
            super().__init__()
            self.order = 3
            self.feature = feature

        def __repr__(self):
            """Return a string representation of the Edit."""
            return f"{type(self).__name__}(feature={self.feature})"

        def __str__(self):
            return repr(self)

        def persist(self):
            self.feature.upsert()

        @property
        def layer(self):
            return self.feature.featureLayer

    class Delete(Edit):
        def __init__(self, feature):
            super().__init__()
            self.order = 4
            self.feature = feature

        def __repr__(self):
            """Return a string representation of the Edit."""
            return f"{type(self).__name__}(feature={self.feature})"

        def __str__(self):
            return repr(self)

        def persist(self):
            self.feature.delete()

        @property
        def layer(self):
            return self.feature.featureLayer

    class CleanupDerivedLayer(Edit):

        def __init__(self, layer, derivedLayer):
            super().__init__()
            self.order = 5
            self._layer = layer
            self.derivedLayer = derivedLayer

        def __repr__(self):
            """Return a string representation of the Edit."""
            return f"{type(self).__name__}(layer={self.layer})"

        def __str__(self):
            return repr(self)

        def persist(self):
            self.derivedLayer.removeAllOfType()

        @property
        def layer(self):
            return self._layer

    def __init__(self):
        WorkspaceMixin.__init__(self)
        self.edits = defaultdict(list)

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{type(self).__name__}(edits={dict.__repr__(self.edits)})"

    def __str__(self):
        return repr(self)

    def editAfter(self, otherEdits):
        otherEdits = otherEdits or Edits()

        for layerId, edits in otherEdits.edits.items():
            self.edits[layerId].extend(edits)
        return self

    def editBefore(self, otherEdits):
        otherEdits = otherEdits or Edits()

        for layerId, edits in otherEdits.edits.items():
            self.edits[layerId] = edits + self.edits[layerId]
        return self

    def append(self, edit):
        self.edits[edit.layer.id()].append(edit)
        return self

    @staticmethod
    def truncate(layer):
        return Edits().append(Edits.Truncate(layer))

    @staticmethod
    def bulkAdd(layer, features):
        return Edits().append(Edits.BulkAdd(layer, features))

    @staticmethod
    def upsert(feature):
        if isinstance(feature, LandTypeCondition):
            return Edits().append(Edits.UpsertTable(feature))
        return Edits().append(Edits.Upsert(feature))

    @staticmethod
    def delete(feature):
        return Edits().append(Edits.Delete(feature))

    @staticmethod
    def cleanupDerivedLayer(layer, derivedLayer):
        return Edits().append(Edits.CleanupDerivedLayer(layer, derivedLayer))

    @property
    def allEdits(self):
        return [edit for edits in self.edits.values() for edit in edits]

    def editsForLayer(self, layer):
        """Return only the edits in this structure for a given layer."""
        layerEdits = Edits()
        layerEdits.edits[layer.id()] = self.edits[layer.id()]
        return layerEdits

    def getFeatures(self, edits):
        for edit in edits:
            if isinstance(edit, Edits.Upsert):
                yield edit.feature
            elif isinstance(edit, Edits.Delete):
                yield edit.feature
            elif isinstance(edit, Edits.BulkAdd):
                for feature in edit.features:
                    yield feature

    @property
    def features(self):
        return self.getFeatures(self.allEdits())

    @property
    def layers(self):
        return [self.workspace.mapLayer(layerId) for layerId in self.edits.keys()]

    @property
    def isEmpty(self):
        """Return True if there are no edits in this structure."""
        return not any(self.edits.values())

    def layerFeatures(self, layer):
        return self.getFeatures(self.edits[layer.id()])

    def layerKeyValues(self, layer, fieldName):
        return set(f.attribute(fieldName) for f in self.layerFeatures(layer))

    def persist(self, raiseErrorIfTaskHasBeenCancelled=lambda: None):
        """Persist these edits to their layers."""
        with Edits.editAndCommit(self.layers):

            for layer in self.layers:
                layerEdits = self.editsForLayer(layer)

                for edits in layerEdits.edits.values():
                    # Order matters here, eg we don't want to truncate at the end
                    sortedEdits = sorted(edits, key=lambda e: e.order)
                    for edit in sortedEdits:
                        raiseErrorIfTaskHasBeenCancelled()
                        edit.persist()

                layer.editsPersisted.emit()

            return self

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
