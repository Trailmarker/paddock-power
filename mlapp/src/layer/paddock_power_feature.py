# -*- coding: utf-8 -*-
from ..models.paddock_power_error import PaddockPowerError
from .paddock_power_feature_status import PaddockPowerFeatureStatus

class PaddockPowerFeature:
    STATUS = "Status"

    def status(self):
        #return PaddockPowerFeatureStatus[self[PaddockPowerFeature.STATUS]]
        return PaddockPowerFeatureStatus.Planned

    def setStatus(self, status):
        if not isinstance(status, PaddockPowerFeatureStatus):
            raise PaddockPowerError("PaddockPowerFeature.setStatus: status must be a PaddockPowerFeatureStatus")
        
        #self.setAttribute(PaddockPowerFeature.STATUS, status.name)

    def recalculate(self, elevationLayer=None):
        """Recalculate the feature's length, perimeter, area."""
        raise NotImplementedError("PaddockPowerFeature.recalculate: must be implemented in subclass")