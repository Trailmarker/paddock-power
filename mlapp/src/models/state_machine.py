# -*- coding: utf-8 -*-
from abc import ABC, abstractproperty
from enum import Enum
from functools import partial

from qgis.PyQt.QtCore import pyqtSignal

from ..models.glitch import Glitch
from ..utils import qgsDebug
from .qt_meta import QtMeta


class StateMachineEnum(Enum):
    def __format__(self, _):
        return self.value

    def __str__(self):
        return self.value


class StateMachineStatus(StateMachineEnum):
    pass


def actionHandler(action, method):
    def wrapper(machine, *args, **kwargs):
        if machine.isPermitted(action):
            message = f"An error happened trying to {action} a {machine}"
            result = ((Glitch.glitchy(message))(method))(machine, *args, **kwargs)
            machine.doAction(action)
            return result
        else:
            raise Glitch(
                f"This {machine} can't handle the action {action} using the handler {method.__name__}, because it's in {machine.status} state")
    return wrapper


class StateMachineAction(StateMachineEnum):
    def handler(self):
        return partial(actionHandler, self)


class StateMachine(ABC, metaclass=QtMeta):
    stateChanged = pyqtSignal(object)

    @abstractproperty
    def transitions(self):
        pass

    @abstractproperty
    def actionType(self):
        pass

    @abstractproperty
    def statusType(self):
        pass

    @abstractproperty
    def status(self):
        pass

    @status.setter
    def status(self, _):
        pass

    def isPermitted(self, action):
        """Return True if the action is enabled for the current status."""
        if not isinstance(action, self.actionType):
            raise Glitch(f"The value {str(action)} is not a valid action for a {self.__class__.__name__}")
        return (self.status, action) in self.transitions

    def allPermitted(self):
        """Return a list of all enabled actions for the current status."""
        return [action for (status, action) in self.transitions if status == self.status]

    def doAction(self, action):
        if self.isPermitted(action):
            newStatus = self.transitions[(self.status, action)]
            qgsDebug(f"{self}: {self.status} → {action} → {newStatus}")
            self.status = newStatus
            self.stateChanged.emit(self.status)
        else:
            qgsDebug(f"{self}: {self.status} → {action} → {newStatus} not permitted")
            raise Glitch(f"An error happened trying to {action} a {self}")

    def __repr__(self):
        """Return a string representation of the EditStateMachine."""
        return f"{self.__class__.__name__}(status={self.status})"

    def __str__(self):
        """Convert the EditStateMachine to a string representation."""
        return repr(self)
