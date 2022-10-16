# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsField

from .capacity_feature import CapacityFeature


class Paddock(CapacityFeature):
    CONDITION, BUILD_FENCE = ["Condition",
                              "Build Fence"]

    SCHEMA = CapacityFeature.SCHEMA + [
        QgsField(name=CONDITION, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=BUILD_FENCE, type=QVariant.LongLong, typeName="Integer64",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
    ]

    def paddockCondition(self):
        return str(self.feature[Paddock.CONDITION])

    def paddockBuildFence(self):
        return self.feature[Paddock.BUILD_FENCE]

    def setPaddockCondition(self, condition):
        self.feature.setAttribute(Paddock.CONDITION, condition)

    def setPaddockBuildFence(self, buildFence):
        self.feature.setAttribute(Paddock.BUILD_FENCE, buildFence)
