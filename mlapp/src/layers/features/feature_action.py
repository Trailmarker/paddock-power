# -*- coding: utf-8 -*-
from ...models import StateMachineAction


class FeatureAction(StateMachineAction):
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
