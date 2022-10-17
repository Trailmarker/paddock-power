# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSignalTransition

from .feature_state import FeatureState
from .feature_action import FeatureAction

from ...utils import qgsDebug

class FeatureTransition(QSignalTransition):
    """A transition between two FeatureStates."""

    def __init__(self, transition: FeatureAction, sourceState: FeatureState, boundSignal, targetState: FeatureState):
        """Create a new FeatureTransition."""
        super().__init__(boundSignal, sourceState)

        self.setTargetState(targetState)
        self._feature = self.sourceState()._feature
        self._transition = transition

    def onTransition(self, event):
        """Handle the transition."""
        qgsDebug(f"FeatureTransition.on{self._transition.name.capitalize()}: {self._feature.__class__.__name__} {self.sourceState().objectName()} -> {self.targetStates()[0].objectName()}")
        super().onTransition(event)

        if hasattr(self._feature, f"on{self._transition.name.capitalize()}"):
            getattr(self._feature, f"on{self._transition.name.capitalize()}")()