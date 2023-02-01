# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, pyqtSignal

from ...models import QtAbstractMeta, StateMachine
from ..fields import FeatureStatus, Timeframe
from .feature_action import FeatureAction


class FeatureStateMachine(QObject, StateMachine, metaclass=QtAbstractMeta):

    _stateChanged = pyqtSignal()

    def __init__(self, feature):
        QObject.__init__(self)
        super().__init__()
        self._feature = feature

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
        newTimeframe = self._feature.featureLayer.timeframe
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
            self._feature.featureLayer.workspace.setTimeframe(newTimeframe)

    @property
    def transitions(self):
        return FeatureStateMachine.__TRANSITIONS

    @property
    def actionType(self):
        return FeatureAction

    @property
    def statusType(self):
        return FeatureStatus

    @property
    def status(self):
        return self._feature.STATUS

    @status.setter
    def status(self, stat):
        self._feature.STATUS = stat

    @property
    def STATUS(self):
        return self._feature.STATUS

    @STATUS.setter
    def status(self, s):
        self._feature.STATUS = s

    def displayName(self):
        return self._feature.displayName()

    @property
    def stateChanged(self):
        return self._stateChanged

    def emitStateChanged(self):
        self.stateChanged.emit()
