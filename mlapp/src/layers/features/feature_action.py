# -*- coding: utf-8 -*-
from functools import partial


from ...models import StateMachineAction, actionHandler
# from ...utils import PLUGIN_NAME
# from .persist_edits_task import PersistEditsTask


class FeatureAction(StateMachineAction):
    def handle(self):
        return partial(actionHandler, self)

    # Result of @FeatureAction.action.save()
    def handleWithSave(action):
        def withSave(method):
            def wrapped(feature, *args, **kwargs):
                edits = actionHandler(action, method)(feature, *args, **kwargs)
                edits.persist()
                edits.notifyPersisted()
            return wrapped
        return withSave

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
