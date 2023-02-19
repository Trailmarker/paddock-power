# -*- coding: utf-8 -*-
from functools import partial

from qgis.core import QgsApplication

from ...models import Glitch, StateMachineAction, actionHandler
from ..interfaces import IPersistedFeature
from .persist_edits_task import PersistEditsTask, persistEdits


class FeatureAction(StateMachineAction):
    def handle(self):
        return partial(actionHandler, self)

    def handleAndPersist(self):
        def withPersistedEdits(method):
            def callWithPersistedEdits(feature, *args, **kwargs):
                if not isinstance(feature, IPersistedFeature):
                    raise Glitch(f"FeatureAction.handleAndPersist: {feature} is not an IPersistedFeature")
                persistEdits(feature, partial(actionHandler, self)(method), *args, **kwargs)

            return callWithPersistedEdits
        return withPersistedEdits

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
    undoArchive = "Undo Archiving"
