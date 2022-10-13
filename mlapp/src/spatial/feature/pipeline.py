# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature, QgsFields

from ...models.paddock_power_error import PaddockPowerError
from .line_feature import LineFeature


class Pipeline(LineFeature):
    SCHEMA = LineFeature.SCHEMA

    def __init__(self):
        super().__init__()


PipelineFeature = type('PipelineFeature', (Pipeline, QgsFeature), {})


def asPipeline(feature):
    """Return a Pipeline object from a QgsFeature."""
    if not isinstance(feature, QgsFeature):
        raise PaddockPowerError("asPipeline: feature is not a QgsFeature")
    if not isinstance(feature, Pipeline):
        feature.__class__ = PipelineFeature
    if not hasattr(feature, 'profile'):
        setattr(feature, 'profile', None)
    return feature


def makePipeline():
    """Return a new and empty Pipeline object."""
    fields = QgsFields()
    for field in Pipeline.SCHEMA:
        fields.append(field)

    feature = QgsFeature(fields)
    return asPipeline(feature)
