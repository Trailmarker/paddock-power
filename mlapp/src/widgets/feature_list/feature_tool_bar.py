# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from ..state_tool_bar.state_tool_bar import StateToolBar


class FeatureToolBar(StateToolBar):
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
