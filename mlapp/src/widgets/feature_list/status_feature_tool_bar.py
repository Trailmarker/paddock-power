# -*- coding: utf-8 -*-
from ...utils import PLUGIN_FOLDER
from ..state_machine_tool_bar.state_machine_tool_bar import StateMachineToolBar


class StatusFeatureToolBar(StateMachineToolBar):
    def __init__(self, feature, parent=None):
        super().__init__(feature.machine, parent)

        self.feature = feature
        self.refreshUi()

    def addSelectAction(self):
        self.addGenericAction(
            f':/plugins/{PLUGIN_FOLDER}/images/zoom-item.png',
            f"Zoom to {self.machine.displayName()}",
            self.selectFeature)

    def selectFeature(self):
        """Select this Fence and zoom to it."""
        self.feature.selectFeature()
