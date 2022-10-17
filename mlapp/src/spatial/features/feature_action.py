# -*- coding: utf-8 -*-
from enum import Enum


class FeatureAction(Enum):
    """Allowed transitions for a Paddock Power feature."""
    draft = "draft"
    plan = "plan"
    undoPlan = "undoPlan"
    build = "build"
    undoBuild = "undoBuild"
    supersede = "supersede"
    undoSupersede = "undoSupersede"
    archive = "archive"
