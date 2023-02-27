# -*- coding: utf-8 -*-
from functools import partial


from ...models import StateMachineAction, actionHandler
from ...utils import PLUGIN_NAME
from .persist_edits_task import PersistEditsTask

class FeatureAction(StateMachineAction):
    def handle(self):
        return partial(actionHandler, self)

    # Result of @FeatureAction.action.save()
    def handleWithSave(action):
        def withSave(method):
            def saveInBackground(feature, *args, **kwargs):
                feature.featureLayer.task = PersistEditsTask(
                    f"{PLUGIN_NAME} saving your data …", True, # notify=True 
                    actionHandler(action, method), feature, *args, **kwargs)
            return saveInBackground
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
