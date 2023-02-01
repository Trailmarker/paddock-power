# -*- coding: utf-8 -*-
from functools import partial
from ..models import StateMachine, StateMachineAction, StateMachineStatus, actionHandler


class EditStatus(StateMachineStatus):
    Viewing = "Viewing"
    Editing = "Editing"


class EditAction(StateMachineAction):
    def handler(self):
        return partial(actionHandler, self)
    
    edit = "Edit"
    save = "Save"
    cancelEdit = "Cancel"


class EditStateMachine(StateMachine):

    def __init__(self):
        super().__init__()
        self._status = EditStatus.Viewing

    # State machine interface
    __TRANSITIONS = {
        (EditStatus.Viewing, EditAction.edit): EditStatus.Editing,
        (EditStatus.Editing, EditAction.save): EditStatus.Viewing,
        (EditStatus.Editing, EditAction.cancelEdit): EditStatus.Viewing
    }

    @property
    def transitions(self):
        return EditStateMachine.__TRANSITIONS

    @property
    def actionType(self):
        return EditAction

    @property
    def statusType(self):
        return EditStatus

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
