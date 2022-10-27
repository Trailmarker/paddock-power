# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ...spatial.features.persisted_feature import PersistedFeature
from ...spatial.features.fence import Fence

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_paddock_changes_base.ui')))


class FencePaddockChanges(QWidget, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.fence = None
        self.project = None

        self.setupUi(self)
        self.refreshUi()

    def setProject(self, project):
        """Set the Project."""
        self.project = project
        self.project.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)
        self.refreshUi()

    @pyqtSlot(PersistedFeature)
    def onSelectedFeatureChanged(self, feature):
        """Handle a change in the selected fence."""

        if feature is None or isinstance(feature, Fence):
            self.fence = feature

            if self.fence:
                self.fence.stateChanged.connect(self.refreshUi)

            self.refreshUi()

    def refreshUi(self):
        """Show the Paddock View."""
        if self.fence is None:
            # self.setVisible(False)
            self.supersededPaddockMiniList.clear()
            self.plannedPaddockMiniList.clear()
        else:
            # self.setVisible(True)
            supersededPaddocks, plannedPaddocks = self.fence.getSupersededAndPlannedPaddocks()

            self.supersededPaddockMiniList.setFeatures(supersededPaddocks)
            self.plannedPaddockMiniList.setFeatures(plannedPaddocks)
