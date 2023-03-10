# -*- coding: utf-8 -*-
from functools import partial

from .feature_table_action import FeatureTableAction
from .select_feature_model import SelectFeatureModel
from .edit_feature_model import EditFeatureModel
from .undo_trash_feature_model import UndoTrashFeatureModel
from .plan_build_feature_model import PlanBuildFeatureModel
from .view_feature_profile_model import ViewFeatureProfileModel


class FeatureTableActionModelFactory:

    def factory(self, editWidgetFactory):
        return {
            FeatureTableAction.selectFeature: SelectFeatureModel,
            FeatureTableAction.editFeature: partial(EditFeatureModel, editWidgetFactory),
            FeatureTableAction.undoTrashFeature: UndoTrashFeatureModel,
            FeatureTableAction.planBuildFeature: PlanBuildFeatureModel,
            FeatureTableAction.viewFeatureProfile: ViewFeatureProfileModel
        }

    def __init__(self, editWidgetFactory=None):
        self._editWidgetFactory = editWidgetFactory

    def createModel(self, featureTableAction, parent=None):
        """Given an index corresponding to a FeatureTableAction, return the appropriate model."""

        featureTableActionModelType = self.factory(self._editWidgetFactory)[featureTableAction]
        return featureTableActionModelType(parent)
