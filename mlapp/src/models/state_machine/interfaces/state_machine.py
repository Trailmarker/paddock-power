# -*- coding: utf-8 -*-
from abc import abstractmethod


class StateMachine:

    @property
    @abstractmethod
    def transitions(self):
        pass

    @property
    @abstractmethod
    def actionType(self):
        pass

    @property
    @abstractmethod
    def statusType(self):
        pass

    @property
    @abstractmethod
    def status(self):
        pass

    @status.setter
    def status(self, _):
        pass

    @property
    @abstractmethod
    def stateChanged(self):
        pass

    @abstractmethod
    def emitStateChanged(self):
        """Emit a signal when the state changes (eg could be a Qt signal)."""
        pass

    @abstractmethod
    def isPermitted(self, action):
        """Return True if the action is enabled for the current status."""
        pass

    @abstractmethod
    def allPermitted(self):
        """Return a list of all enabled actions for the current status."""
        pass

    @abstractmethod
    def doAction(self, action):
        pass

    def __repr__(self):
        """Return a string representation of the EditStateMachine."""
        return f"{self.__class__.__name__}(status={self.status})"

    def __str__(self):
        """Convert the state machine to a string representation."""
        return repr(self)
