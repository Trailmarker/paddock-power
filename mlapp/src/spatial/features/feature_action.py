# -*- coding: utf-8 -*-
from ...models.state_machine import StateMachineAction


class FeatureAction(StateMachineAction):
    """Allowed transitions for a Paddock Power feature."""
    draft = "Draft"
    trash = "Trash"
    plan = "Plan"
    undoPlan = "Undo Planning"
    build = "Build"
    undoBuild = "Undo Building"
    supersede = "Supersede"
    undoSupersede = "Undo Superseding"
    archive = "Archive"
