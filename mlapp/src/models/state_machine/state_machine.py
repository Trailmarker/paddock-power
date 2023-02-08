# -*- coding: utf-8 -*-
from ..glitch import Glitch
from ...utils import qgsInfo

from .interfaces.state_machine import StateMachine as IStateMachine


class StateMachine(IStateMachine):

    def __init__(self):
        super().__init__()

    @property
    def transitions(self):
        pass

    @property
    def actionType(self):
        pass

    @property
    def statusType(self):
        pass

    @property
    def status(self):
        pass

    @status.setter
    def status(self, _):
        pass

    @property
    def stateChanged(self):
        raise NotImplementedError

    def emitStateChanged(self):
        raise NotImplementedError

    def isPermitted(self, action):
        """Return True if the action is enabled for the current status."""
        if not isinstance(action, self.actionType):
            raise Glitch(f"The value {str(action)} is not a valid action for a {self.__class__.__name__}")
        return (self.status, action) in self.transitions

    def allPermitted(self):
        """Return a list of all enabled actions for the current status."""
        return [action for (status, action) in self.transitions if status.match(self.status)]

    def doAction(self, action):
        if self.isPermitted(action):
            newStatus = self.transitions[(self.status, action)]
            qgsInfo(f"{self}: {self.status} → {action} → {newStatus}")
            self.status = newStatus
            self.emitStateChanged()
        else:
            qgsInfo(f"{self}: {self.status} → {action} → ?? not permitted")
            raise Glitch(f"An error happened trying to {action} a {self}")

    def __repr__(self):
        """Return a string representation of the EditStateMachine."""
        return f"{self.__class__.__name__}(status={self.status})"

    def __str__(self):
        """Convert the state machine to a string representation."""
        return repr(self)
