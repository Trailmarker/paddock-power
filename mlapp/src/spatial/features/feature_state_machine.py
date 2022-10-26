# -*- coding: utf-8 -*-
from ...models.state_machine import StateMachine
from .feature_action import FeatureAction
from ..schemas.feature_status import FeatureStatus


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

    @property
    def transitions(self):
        return FeatureStateMachine.__TRANSITIONS

    @property
    def actionType(self):
        return FeatureAction

    @property
    def statusType(self):
        return FeatureStatus
