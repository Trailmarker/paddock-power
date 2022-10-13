# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsField

from ...models.paddock_power_error import PaddockPowerError
from .feature_status import FeatureStatus


class Feature:
    FID = "fid"
    STATUS = "Status"
    NAME = "Name"

    SCHEMA = [
        QgsField(name=NAME, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=STATUS, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def clearId(self):
        """Clear the feature's id."""
        self.setAttribute(Feature.FID, None)

    def status(self):
        try:
            return FeatureStatus[self[Feature.STATUS]]
        except:
            return FeatureStatus.Unknown

    def featureName(self):
        return self[Feature.NAME]

    def setStatus(self, status):
        if not isinstance(status, FeatureStatus):
            raise PaddockPowerError(
                "PaddockPowerFeature.setStatus: status must be a PaddockPowerFeatureStatus")
        if status == FeatureStatus.Unknown:
            raise PaddockPowerError(
                "PaddockPowerFeature.setStatus: trying to set FeatureStatus.Unknown")
        self.setAttribute(Feature.STATUS, status.name)

    def setFeatureName(self, name):
        self.setAttribute(Feature.NAME, name)

    def recalculate(self, elevationLayer=None):
        """Recalculate the feature's length, perimeter, area."""
        raise NotImplementedError(
            "PaddockPowerFeature.recalculate: must be implemented in subclass")
