# -*- coding: utf-8 -*-
from ...models.state_machine import StateMachine
from ..fields.feature_status import FeatureStatus
from ..fields.timeframe import Timeframe
from .feature_action import FeatureAction


class FeatureStateMachine(StateMachine):
    def __init__(self):
        self._status = FeatureStatus.Undefined

    # State machine interface
    __TRANSITIONS = {
        (FeatureStatus.Undefined, FeatureAction.draft): FeatureStatus.Drafted,
        (FeatureStatus.Undefined, FeatureAction.plan): FeatureStatus.Planned,

        (FeatureStatus.Drafted, FeatureAction.trash): FeatureStatus.Undefined,
        (FeatureStatus.Drafted, FeatureAction.plan): FeatureStatus.Planned,
        (FeatureStatus.Drafted, FeatureAction.archive): FeatureStatus.Archived,

        (FeatureStatus.Planned, FeatureAction.undoPlan): FeatureStatus.Drafted,
        (FeatureStatus.Planned, FeatureAction.build): FeatureStatus.Built,
        (FeatureStatus.Planned, FeatureAction.supersede): FeatureStatus.PlannedSuperseded,
        (FeatureStatus.Planned, FeatureAction.archive): FeatureStatus.Archived,

        (FeatureStatus.Built, FeatureAction.undoBuild): FeatureStatus.Planned,
        (FeatureStatus.Built, FeatureAction.supersede): FeatureStatus.BuiltSuperseded,
        (FeatureStatus.Built, FeatureAction.archive): FeatureStatus.Archived,

        (FeatureStatus.PlannedSuperseded, FeatureAction.undoSupersede): FeatureStatus.Planned,
        (FeatureStatus.PlannedSuperseded, FeatureAction.archive): FeatureStatus.Archived,

        (FeatureStatus.BuiltSuperseded, FeatureAction.undoSupersede): FeatureStatus.Built,
        (FeatureStatus.BuiltSuperseded, FeatureAction.archive): FeatureStatus.Archived,
    }

    def doAction(self, action):
        """Perform an action on the Feature state machine and update the current timeframe if necessary."""
        newTimeframe = self.featureLayer.currentTimeframe
        actionPermitted = self.isPermitted(action)

        if actionPermitted:
            newStatus = self.transitions[(self.status, action)]

            if not newTimeframe.matchFeatureStatus(newStatus):

                for tf in [Timeframe.Current, Timeframe.Future]:
                    if tf.matchFeatureStatus(newStatus):
                        newTimeframe = tf
                        break

        super().doAction(action)

        if actionPermitted:
            self.featureLayer.setCurrentTimeframe(newTimeframe)

    @property
    def transitions(self):
        return FeatureStateMachine.__TRANSITIONS

    @property
    def actionType(self):
        return FeatureAction

    @property
    def statusType(self):
        return FeatureStatus
