# -*- coding: utf-8 -*-
from ...spatial.features.feature_status import FeatureStatus
from ...models.paddock_power_state import PaddockPowerState
from .paddock_list_base import PaddockListBase


class PaddockList(PaddockListBase):
    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(parent)

        self.state = PaddockPowerState()

        # refreshUi is implemented in PaddockListBase
        self.state.milestoneChanged.connect(self.refreshUi)
        self.state.milestoneDataChanged.connect(self.refreshUi)

        self.refreshUi()

    def getPaddocks(self):
        """Get the paddocks."""
        milestone = self.state.getMilestone()
        return [paddock for paddock in milestone.paddockLayer.getFeaturesByStatus(FeatureStatus.Existing, FeatureStatus.Planned)] if milestone is not None else None
