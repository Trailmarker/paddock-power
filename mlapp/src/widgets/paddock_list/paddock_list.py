# -*- coding: utf-8 -*-
from ...models.state import getProject
from .paddock_list_base import PaddockListBase

class PaddockList(PaddockListBase):
    def __init__(self, parent=None):
        """Constructor."""

        super(PaddockListBase, self).__init__(parent)

        self.project = getProject()
        if self.project is not None:
            self.project.currentMilestoneChanged.connect(self.refreshUi)
            self.refreshUi()

    def getPaddocks(self):
        """Get the paddocks."""
        milestone = self.project.currentMilestone
        return milestone.paddockLayer.getFeatures() if milestone is not None else None
