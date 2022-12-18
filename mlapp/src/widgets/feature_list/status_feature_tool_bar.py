# -*- coding: utf-8 -*-
from ..state_machine_tool_bar.state_machine_tool_bar import StateMachineToolBar


class StatusFeatureToolBar(StateMachineToolBar):
    def __init__(self, feature, parent=None):
        super().__init__(feature, parent)

        self.refreshUi()

    def addSelectAction(self):
        self.addGenericAction(
            ':/plugins/mlapp/images/zoom-item.png',
            f"Zoom to {self.machine.displayName()}",
            self.selectFeature)

    def selectFeature(self):
        """Select this Fence and zoom to it."""
        self.machine.selectFeature()
