# -*- coding: utf-8 -*-
from functools import partial


from ...models import Glitch, StateMachineAction, actionHandler
from ...utils import qgsDebug
from ..interfaces import IPersistedFeature
from .persist_edits_task import persistEdits


class FeatureAction(StateMachineAction):
    def handle(self):
        return partial(actionHandler, self)

    def handleAndPersist(action):                                                 # Result of @FeatureAction.action.handleAndPersist()
        def withPersistedEdits(method):                                           # Resulting decorator
            def callWithPersistedEdits(*args, **kwargs):                          # Resulting decorated method
                qgsDebug(f"callWithPersistedEdits({action}, {args}, {kwargs})")
                edits = actionHandler(action, method)(*args, **kwargs)
                qgsDebug(f"callWithPersistedEdits({action}, {args}, {kwargs}): edits={edits}")
                edits.persist()
                edits.notifyPersisted()
                qgsDebug("callWithPersistedEdits complete")                
                # persistEdits(actionHandler(action, method), *args, **kwargs)
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
