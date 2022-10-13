# -*- coding: utf-8 -*-
from qgis.core import QgsFeature, QgsField, QgsFields

from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature

from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug
from ..calculator import Calculator
from .feature import Feature
from .line_feature import LineFeature


class Fence(LineFeature):
    NAME, LENGTH, STATUS, BUILD_ORDER = [Feature.NAME,
                                         LineFeature.LENGTH,
                                         Feature.STATUS,
                                         "Build Order"]

    SCHEMA = LineFeature.SCHEMA + [
        QgsField(name=BUILD_ORDER, type=QVariant.LongLong, typeName="Integer64",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def __init__(self):
        super().__init__()

        # Cache the length profile
        self.profile = None
        self.supersededPaddocks = []
        self.plannedPaddocks = []

    def fenceBuildOrder(self):
        return self[Fence.BUILD_ORDER]

    def setFenceBuildOrder(self, buildOrder):
        self.setAttribute(Fence.BUILD_ORDER, buildOrder)

    def getProfile(self):
        return self.profile

    def setSupersededPaddocks(self, paddocks):
        """Set the list of paddocks that have been Superseded by this Fence."""
        self.supersededPaddocks = paddocks

    def getSupersededPaddocks(self):
        """Return a list of paddocks that have been Superseded by this Fence."""
        return self.supersededPaddocks

    def setPlannedPaddocks(self, paddocks):
        """Set the list of paddocks that have been Planned by this Fence."""
        self.plannedPaddocks = paddocks

    def getPlannedPaddocks(self):
        """Return a list of paddocks that have been Planned by this Fence."""
        return self.plannedPaddocks


FenceFeature = type('FenceFeature', (Fence, QgsFeature), {})


def ensureAttrs(fence, *attrs):
    for attr in attrs:
        if not hasattr(fence, attr):
            setattr(fence, attr, None)


def asFence(feature):
    """Return a Fence object from a QgsFeature."""
    if not isinstance(feature, QgsFeature):
        qgsDebug(f"feature: {str(feature)}")
        qgsDebug(f"feature.__class__.__name__: {feature.__class__.__name__}")
        raise PaddockPowerError("asFence: feature is not a QgsFeature")
    # Hack in the other attributes
    if not isinstance(feature, Fence):
        feature.__class__ = FenceFeature
    ensureAttrs(feature, "profile", "supersededPaddocks", "plannedPaddocks")
    feature.supersededPaddocks = []
    feature.plannedPaddocks = []
    return feature


def makeFence():
    """Return a new and empty Fence object."""
    fields = QgsFields()
    for field in Fence.SCHEMA:
        fields.append(field)

    feature = QgsFeature(fields)
    return asFence(feature)
