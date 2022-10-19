# -*- coding: utf-8 -*-
from enum import Enum


class FeatureAction(Enum):
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

    def __str__(self):
        return self.value
