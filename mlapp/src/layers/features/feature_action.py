# -*- coding: utf-8 -*-
from functools import partial
from ...models import StateMachineAction, actionHandler


class FeatureAction(StateMachineAction):
    def handler(self):
        return partial(actionHandler, self)

    """Allowed transitions for a StatusFeature."""
    draft = "Draft"
    trash = "Trash"
    plan = "Plan"
    undoPlan = "Undo Planning"
    build = "Build"
    undoBuild = "Undo Building"
    supersede = "Supersede"
    undoSupersede = "Undo Superseding"
    archive = "Archive"
