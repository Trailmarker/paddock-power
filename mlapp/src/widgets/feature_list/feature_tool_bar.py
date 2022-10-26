# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from ...spatial.features.persisted_feature import PersistedFeature
from ..state_tool_bar import StateToolBar


class FeatureToolBar(StateToolBar):
    featureZoomed = pyqtSignal(PersistedFeature)

    def __init__(self, feature, parent=None):
        super().__init__(feature, parent)

        self.refreshUi()

    def addZoomAction(self):
        self.addGenericAction(
            ':/plugins/mlapp/images/paddock-zoom.png',
            f"Zoom to {self.machine.displayName()}",
            self.zoomFeature)

    def zoomFeature(self):
        """Select this Fence and zoom to it."""
        self.featureZoomed.emit(self.machine)
