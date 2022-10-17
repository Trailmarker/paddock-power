# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QState

from .feature_status import FeatureStatus


class FeatureState(QState):
    """A state for a feature."""

    def __init__(self, featureStatus: FeatureStatus, feature):
        """Initialise the state."""
        super().__init__()
        self.setObjectName(featureStatus.name)
        self._featureStatus = featureStatus
        self._feature = feature

        self.entered.connect(self.setFeatureStatus)
        self.entered.connect(self._feature.stateChanged.emit)

    def setFeatureStatus(self):
        self._feature.status = self._featureStatus

