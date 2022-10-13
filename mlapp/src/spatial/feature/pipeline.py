# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature, QgsField, QgsFields

from ...models.paddock_power_error import PaddockPowerError
from ..calculator import Calculator
from .feature import Feature
from .line_feature import LineFeature


class Pipeline(LineFeature):
    NAME, LENGTH, STATUS = [Feature.NAME,
                            LineFeature.LENGTH,
                            Feature.STATUS]

    SCHEMA = [
        QgsField(name=NAME, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=LENGTH, type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=STATUS, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def __init__(self):
        super().__init__()

        # Cache the length profile
        self.profile = None

    def getProfile(self):
        return self.profile

    def recalculate(self, elevationLayer=None):
        """Recalculate the length of this Pipeline."""
        self.profile = Calculator.calculateProfile(
            self.geometry(), elevationLayer)
        length = round(self.profile.maximumDistance, 2)
        self.setAttribute(Pipeline.LENGTH, length)


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
