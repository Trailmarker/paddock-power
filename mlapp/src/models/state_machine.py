# -*- coding: utf-8 -*-
from abc import ABC, abstractproperty
from enum import Enum

from ..models.glitch import Glitch
from ..utils import qgsDebug
from .qt_meta import QtMeta

class StateMachineAction(Enum):
    
    @classmethod
    def handler(actionType, action):
        """Decorator that takes a method on a Feature, and returns a method that instead raises an exception if the
        Feature's current status means {action} is not permitted, and otherwise calls the original method, updates
        the Feature's status, and returns the result of the original method."""
        
        if not isinstance(action, actionType):
            raise Glitch(f"Can't make an actionHandler({actionType.__class__.__name__}) for {action}, because it's not a {actionType.__class__.__name__}")

        def makeActionHandler(func):
            def handlerWithTryAction(machine: StateMachine, *args, **kwargs):
                if machine.isPermitted(action):
                    message = f"An error happened trying to {action} a {machine}"
                    result = ((Glitch.glitchy(message))(func))(machine, *args, **kwargs)
                    machine.doAction(action)
                    return result
                else:
                    raise Glitch(f"You can't {action} a {machine}, because it is {machine.status}")
            return handlerWithTryAction
        return makeActionHandler

    def __str__(self):
        return self.value


class StateMachine(ABC, metaclass=QtMeta):
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
            qgsDebug(f"{self.__class__.__name__}: {self.status} → {action} → {newStatus}")
            self.status = newStatus
        else:
            raise Glitch(f"An error happened trying to {action} a {self}")

    def __repr__(self):
        """Return a string representation of the EditStateMachine."""
        return f"{self.__class__.__name__}(status={self.status})"

    def __str__(self):
        """Convert the EditStateMachine to a string representation."""
        return repr(self)

