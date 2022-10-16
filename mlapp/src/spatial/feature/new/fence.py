# -*- coding: utf-8 -*-
from qgis.core import QgsField

from qgis.PyQt.QtCore import QVariant

from .line_feature import LineFeature


class Fence(LineFeature):
    BUILD_ORDER = "Build Order"

    SCHEMA = LineFeature.SCHEMA + [
        QgsField(name=BUILD_ORDER, type=QVariant.LongLong, typeName="Integer64",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def __init__(self, feature=None):
        super().__init__(feature)

        # Cache paddock data - TODO build this stuff in recalculate
        self.supersededPaddocks = []
        self.plannedPaddocks = []

    def fenceBuildOrder(self):
        return self.feature[Fence.BUILD_ORDER]

    def setFenceBuildOrder(self, buildOrder):
        self.feature.setAttribute(Fence.BUILD_ORDER, buildOrder)

    def setSupersededPaddocks(self, paddocks):
        """Set the list of paddocks that have been Superseded by this Fence."""
        self.supersededPaddocks = paddocks

    def supersededPaddocks(self):
        """Return a list of paddocks that have been Superseded by this Fence."""
        return self.supersededPaddocks

    def setPlannedPaddocks(self, paddocks):
        """Set the list of paddocks that have been Planned by this Fence."""
        self.plannedPaddocks = paddocks

    def plannedPaddocks(self):
        """Return a list of paddocks that have been Planned by this Fence."""
        return self.plannedPaddocks
