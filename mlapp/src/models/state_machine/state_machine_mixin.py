# -*- coding: utf-8 -*-
from abc import abstractmethod

from .interfaces.state_machine import StateMachine as IStateMachine


class StateMachineMixin:
    """Given an object a degree of control in terms of how it works as a machine."""

    # In the case of getting from the machine to the object, we have the latitude
    # to implement the StateMachine interface the way we choose (eg FeatureStateMachine
    # is done as a facade).This is for the other way round, getting from the object
    # to the machine …
    @property
    @abstractmethod
    def machine(self):
        pass


def toStateMachine(obj):
    """Retrieve the machine from the object."""
    if isinstance(obj, StateMachineMixin):
        return obj.machine
    elif isinstance(obj, IStateMachine):
        return obj
