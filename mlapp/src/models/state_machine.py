# -*- coding: utf-8 -*-
from abc import ABC, abstractproperty
from enum import Enum

from ..models.glitch import Glitch, glitchy
from .qt_meta import QtMeta

class StateMachineAction(Enum):
    
    @classmethod
    def actionHandler(stateMachineActionType):
        """Decorator that takes a method on a Feature, and returns a method that instead raises an exception if the
        Feature's current status means {action} is not permitted, and otherwise calls the original method, updates
        the Feature's status, and returns the result of the original method."""
        def makeActionHandlerForAction(action: StateMachineAction):
            if not isinstance(action, stateMachineActionType):
                raise Glitch(f"Can't make an actionHandler({stateMachineActionType.__class__.__name__}) for {action}, because it's not a {stateMachineActionType.__class__.__name__}")

            def makeActionHandler(handler):
                def handlerWithTryAction(machine: StateMachine, *args, **kwargs):
                    if machine.isPermitted(action):
                        message = f"An error happened trying to {action} a {machine}"
                        result = ((glitchy(message))(handler))(machine, *args, **kwargs)
                        machine.doAction(action)
                        return result
                    else:
                        raise Glitch(f"You can't {action} a {machine}, because it is {machine.status}")
                return handlerWithTryAction
            return makeActionHandler
        return makeActionHandlerForAction

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
        return (self.status, action) in self.transitions()

    def allPermitted(self):
        """Return a list of all enabled actions for the current status."""
        return [action for (status, action) in self.transitions() if status == self.status]

    def doAction(self, action):
        if self.isPermitted(action):
            self.status = self.transitions()[(self.status, action)]
        else:
            raise Glitch(f"An error happened trying to {action} a {self}")

    def __repr__(self):
        """Return a string representation of the EditStateMachine."""
        return f"{self.__class__.__name__}(status={self.status})"

    def __str__(self):
        """Convert the EditStateMachine to a string representation."""
        return repr(self)

