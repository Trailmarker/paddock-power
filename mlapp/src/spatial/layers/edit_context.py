# -*- coding: utf-8 -*-
import contextlib

from qgis.core import QgsVectorLayer

from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug


@contextlib.contextmanager
def editAndCommit(*layers):
    if not all(isinstance(layer, QgsVectorLayer) for layer in layers):
        raise PaddockPowerError("editAndCommit: All layers must be QgsVectorLayers")

    if any(layer.isEditable() for layer in layers):
        raise PaddockPowerError("editAndCommit: All layers must be in non-editable state")

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


@contextlib.contextmanager
def editAndRollBack(*layers):
    if not all(isinstance(layer, QgsVectorLayer) for layer in layers):
        raise PaddockPowerError("editAndRollBack: All layers must be QgsVectorLayers")

    if any(layer.isEditable() for layer in layers):
        raise PaddockPowerError("editAndRollBack: All layers must be in non-editable state")

    try:
        for layer in layers:
            layer.startEditing()

        qgsDebug("editAndRollBack: editing started")

        yield

        for layer in layers:
            layer.commitChanges()

        qgsDebug("editAndRollBack: changes rolled back")

    except Exception as e:
        for layer in layers:
            layer.rollBack()
        raise e
