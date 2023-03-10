# -*- coding: utf-8 -*-
from abc import abstractproperty

from ....layers.features import FeatureAction
from .feature_table_action_model import FeatureTableActionModel


class FeatureActionsModel(FeatureTableActionModel):

    def __init__(self):
        super().__init__()

    def doAction(self, index):
        """Do the current feature action at the given index."""
        featureAction = self.featureAction(index)
        if not featureAction:
            return

        name = featureAction.name
        feature = self.getFeature(index)

        if FeatureAction[name] == FeatureAction.undoPlan:
            feature.undoPlanFeature()
        elif FeatureAction[name] == FeatureAction.plan:
            feature.planFeature()
        elif FeatureAction[name] == FeatureAction.undoBuild:
            feature.undoBuildFeature()
        elif FeatureAction[name] == FeatureAction.build:
            feature.buildFeature()
        elif FeatureAction[name] == FeatureAction.trash:
            feature.trashFeature()

    def icon(self, index):
        """The icon to paint in the cell."""
        featureAction = self.featureAction(index)
        return self.featureActionIcons[featureAction] if featureAction else None

    def description(self, index):
        """Return the description of the current FeatureAction."""
        featureAction = self.featureAction(index)
        return featureAction.value if featureAction else None

    @abstractproperty
    def featureActionIcons(self):
        """A dictionary of FeatureAction objects and their associated icons."""
        pass

    def featureAction(self, index):
        """Get the FeatureAction currently available at the given index."""
        feature = self.getFeature(index)

        return next(
            (action for action in self.featureActionIcons if feature.machine.isPermitted(action)), None)
