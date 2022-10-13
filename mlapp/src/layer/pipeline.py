# -*- coding: utf-8 -*-
from mlapp.src.layer.paddock_power_feature import PaddockPowerFeature
from mlapp.src.layer.paddock_power_feature_status import PaddockPowerFeatureStatus
from qgis.core import (QgsFeature, QgsField, QgsFields)
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature

from .calculator import Calculator
from .paddock_power_feature import PaddockPowerFeature


class Pipeline(PaddockPowerFeature):
    LENGTH, STATUS = ["Pipeline Length",
                      "Status"]

    SCHEMA = [
        QgsField(name=LENGTH, type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=STATUS, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def __init__(self):
        super().__init__()

        # Cache the length profile
        self.profile = None

    def pipelineLength(self):
        return self[Pipeline.LENGTH]

    def setPipelineLength(self, length):
        self.setAttribute(Pipeline.LENGTH, length)

    def getProfile(self):
        return self.profile

    def recalculate(self, elevationLayer=None):
        """Recalculate the length of this Pipeline."""
        self.profile = Calculator.calculateProfile(
            self.geometry(), elevationLayer)
        self.setFenceLength(self.profile.maximumDistance)


def asPipeline(feature):
    """Return a Pipeline object from a QgsFeature."""
    feature.__class__ = type('PipelineFeature', (Pipeline, QgsFeature), {})
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
