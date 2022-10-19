# -*- coding: utf-8 -*-
from contextlib import contextmanager

from qgis.core import QgsVectorLayer

from ...models.glitch import Glitch
from ...utils import qgsDebug


@contextmanager
def editAndCommit(*layers):
    layers = set(layers)

    if not all(isinstance(layer, QgsVectorLayer) for layer in layers):
        raise Glitch("editAndCommit: All layers must be QgsVectorLayers")

    if any(layer.isEditable() for layer in layers):
        raise Glitch("editAndCommit: All layers must be in non-editable state")

    try:
        for layer in layers:
            layer.startEditing()

        qgsDebug("editAndCommit: Edit context started")

        yield

        for layer in layers:
            layer.commitChanges()

        qgsDebug("editAndCommit: Changes committed")

    except Exception as e:
        for layer in layers:
            layer.rollBack()
        raise e


@contextmanager
def editAndRollBack(*layers):
    layers = set(layers)

    if not all(isinstance(layer, QgsVectorLayer) for layer in layers):
        raise Glitch("editAndRollBack: All layers must be QgsVectorLayers")

    if any(layer.isEditable() for layer in layers):
        raise Glitch("editAndRollBack: All layers must be in non-editable state")

    try:
        for layer in layers:
            layer.startEditing()

        qgsDebug("editAndRollBack: editing started")

        yield

        for layer in layers:
            layer.rollBack()

        qgsDebug("editAndRollBack: changes rolled back")

    except Exception as e:
        for layer in layers:
            layer.rollBack()
        raise e
