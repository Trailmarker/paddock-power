# -*- coding: utf-8 -*-
from functools import partial


from ...models import StateMachineAction, actionHandler
from ...utils import qgsDebug


class FeatureAction(StateMachineAction):
    def handle(self):
        return partial(actionHandler, self)

    # Result of @FeatureAction.action.handleAndPersist()
    def handleAndPersist(action):
        def withPersistedEdits(method):                                           # Resulting decorator
            def callWithPersistedEdits(*args, **kwargs):                          # Resulting decorated method
                edits = actionHandler(action, method)(*args, **kwargs)

                edits.persist()
                edits.notifyPersisted()
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
