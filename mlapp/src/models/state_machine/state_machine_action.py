# -*- coding: utf-8 -*-
from ..glitch import Glitch

from .state_machine_enum import StateMachineEnum
from .state_machine_mixin import toStateMachine


class StateMachineActionFailure(Exception):
    pass


class StateMachineAction(StateMachineEnum):
    pass


def actionHandlerWithException(action, exceptionType=None, method=lambda x: x):
    def wrapper(obj, *args, **kwargs):
        if toStateMachine(obj).isPermitted(action):
            # If the action raises a StateMachineFailure, that means the transition *shouldn't* happen
            try:
                result = ((Glitch.glitchy())(method))(obj, *args, **kwargs)
            except exceptionType as e:
                return None
            toStateMachine(obj).doAction(action)
            return result
        else:
            raise Glitch(
                f"This {obj} can't handle the action {action} using the handler {method.__name__}, because it's in {obj.status} state")
    return wrapper


def actionHandler(action, method=lambda x: x):
    def wrapper(obj, *args, **kwargs):
        if toStateMachine(obj).isPermitted(action):
            result = ((Glitch.glitchy())(method))(obj, *args, **kwargs)
            toStateMachine(obj).doAction(action)
            return result
        else:
            raise Glitch(
                f"This {obj} can't handle the action {action} using the handler {method.__name__}, because it's in {obj.status} state")
    return wrapper
