# -*- coding: utf-8 -*-
from ...models.paddock_power_error import PaddockPowerError
from .feature_status import FeatureStatus


class Feature:
    FID = "fid"
    STATUS = "Status"

    def clearId(self):
        """Clear the feature's id."""
        self.setAttribute(Feature.FID, None)

    def status(self):
        return FeatureStatus[self[Feature.STATUS]]
        # return FeatureStatus.Planned

    def setStatus(self, status):
        if not isinstance(status, FeatureStatus):
            raise PaddockPowerError(
                "PaddockPowerFeature.setStatus: status must be a PaddockPowerFeatureStatus")
        self.setAttribute(Feature.STATUS, status.name)

    def recalculate(self, elevationLayer=None):
        """Recalculate the feature's length, perimeter, area."""
        raise NotImplementedError(
            "PaddockPowerFeature.recalculate: must be implemented in subclass")
