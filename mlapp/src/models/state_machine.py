# -*- coding: utf-8 -*-
from abc import abstractproperty
from enum import Enum
from functools import partial

from ..models.glitch import Glitch
from ..utils import qgsInfo


class StateMachineEnum(Enum):
    def match(self, *statuses):
        """Return True if a provided StateMachineStatus or string matches this status.
            Note Enum values are tested by identity, so this became necessary."""
        return self.value in [s.value if isinstance(s, StateMachineEnum) else str(s) for s in statuses]

    def __format__(self, _):
        return self.value

    def __str__(self):
        return self.value


class StateMachineStatus(StateMachineEnum):
    pass


class StateMachineMixin:
    """Given an object a degree of control in terms of how it works as a machine."""
    
    # In the case of getting from the machine to the object, we have the latitude
    # to implement the StateMachine interface the way we choose (eg FeatureStateMachine
    # is done as a facade).This is for the other way round, getting from the object 
    # to the machine …
    @abstractproperty
    def machine(self):
        pass

def machine(obj):
    """Retrieve the machine from the object."""
    if isinstance(obj, StateMachineMixin):
        return obj.machine
    elif isinstance(obj, StateMachine):
        return obj


def actionHandler(action, method):
    def wrapper(obj, *args, **kwargs):
        if machine(obj).isPermitted(action):
            # message = f"An error happened trying to {action} a {machine}"
            result = ((Glitch.glitchy())(method))(obj, *args, **kwargs)
            machine(obj).doAction(action)
            return result
        else:
            raise Glitch(
                f"This {obj} can't handle the action {action} using the handler {method.__name__}, because it's in {obj.status} state")
    return wrapper


class StateMachineAction(StateMachineEnum):
    def handler(self):
        return partial(actionHandler, self)


class StateMachine:

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
            qgsInfo(f"{self}: {self.status} → {action} → {newStatus} not permitted")
            # raise Glitch(f"An error happened trying to {action} a {self}")

    def __repr__(self):
        """Return a string representation of the EditStateMachine."""
        return f"{self.__class__.__name__}(status={self.status})"

    def __str__(self):
        """Convert the state machine to a string representation."""
        return repr(self)
