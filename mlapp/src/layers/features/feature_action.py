# -*- coding: utf-8 -*-
from functools import partial

from ...models import StateMachineAction, actionHandler


class FeatureAction(StateMachineAction):
    def handle(selfAsFeatureAction):
        return partial(actionHandler, selfAsFeatureAction)

    def handleWithSave(selfAsFeatureAction):
        def withActionHandler(method):
            def withSaveEditsAndDeriveTask(feature, *args, **kwargs):
                editFunction = actionHandler(selfAsFeatureAction, method)
                return feature.featureLayer.workspace.saveEditsAndDerive(editFunction, feature, *args, **kwargs)
            return withSaveEditsAndDeriveTask
        return withActionHandler

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
