# -*- coding: utf-8 -*-
from ...spatial.features.feature_status import FeatureStatus
from ...models.state import State
from .feature_list_base import FeatureListBase


class FeatureList(FeatureListBase):
    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(parent)

        self.state = State()

        # refreshUi is implemented in PaddockListBase
        self.state.milestoneChanged.connect(self.refreshUi)
        self.state.milestoneDataChanged.connect(self.refreshUi)

        self.refreshUi()

    def getFeatures(self):
        """Get the paddocks."""
        milestone = self.state.getMilestone()
        return [paddock for paddock in milestone.paddockLayer.getFeaturesByStatus(FeatureStatus.Built, FeatureStatus.Planned)] if milestone is not None else None
