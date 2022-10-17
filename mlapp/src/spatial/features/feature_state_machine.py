# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QStateMachine

from .feature_state import FeatureState
from .feature_status import FeatureStatus as S
from .feature_transition import FeatureTransition
from .feature_action import FeatureAction as A


class FeatureStateMachine(QStateMachine):

    def __init__(self, feature):
        """Initialise the state machine."""
        # Set up state machine
        super().__init__()

        self._feature = feature
        self._stateMapping = {}

        for featureStatus in S:
            featureState = FeatureState(featureStatus, self._feature)
            self._stateMapping[featureStatus] = featureState
            self.addState(featureState)

        self.addFeatureTransition(S.Undefined, A.draft, S.Drafted)
        self.addFeatureTransition(S.Undefined, A.plan, S.Planned)

        self.addFeatureTransition(S.Drafted, A.plan, S.Planned)
        self.addFeatureTransition(S.Drafted, A.archive, S.Archived)

        self.addFeatureTransition(S.Planned, A.undoPlan, S.Drafted)
        self.addFeatureTransition(S.Planned, A.build, S.Existing)
        self.addFeatureTransition(S.Planned, A.supersede, S.PlannedSuperseded)
        self.addFeatureTransition(S.Planned, A.archive, S.Archived)

        self.addFeatureTransition(S.Existing, A.undoBuild, S.Planned)
        self.addFeatureTransition(S.Existing, A.supersede, S.ExistingSuperseded)
        self.addFeatureTransition(S.Existing, A.archive, S.Archived)

        self.addFeatureTransition(S.PlannedSuperseded, A.undoSupersede, S.Planned)
        self.addFeatureTransition(S.PlannedSuperseded, A.archive, S.Archived)

        self.addFeatureTransition(S.ExistingSuperseded, A.undoSupersede, S.Existing)
        self.addFeatureTransition(S.ExistingSuperseded, A.archive, S.Archived)

        self.setInitialState(self._stateMapping[self._feature.status])

    def getStates(self):
        return [s for s in S if self._stateMapping[s] in self.configuration()]

    def addFeatureTransition(self, currentStatus, transition: A, nextStatus):
        """Add a transition between states."""
        sourceState = self._stateMapping[currentStatus]
        signal = getattr(self._feature, transition.name)
        sourceState.addTransition(FeatureTransition(transition, sourceState, signal, self._stateMapping[nextStatus]))
