# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ....layers.features import FeatureAction
from ....utils import PLUGIN_FOLDER
from .feature_table_action import FeatureTableAction
from .feature_actions_model import FeatureActionsModel


class PlanBuildFeatureModel(FeatureActionsModel):
    """An item model that configures moving forward the progress on planning, building, etc, a feature."""

    _planIcon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/plan-feature.png')
    _buildIcon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/build-feature.png')

    def __init__(self):
        super().__init__()

    @property
    def featureTableAction(self):
        """The table action associated with this delegate"""
        return FeatureTableAction.planBuildFeature

    @property
    def featureActionIcons(self):
        """A dictionary of FeatureAction objects and their associated icons."""

        return {
            FeatureAction.plan: self._planIcon,
            FeatureAction.build: self._buildIcon
        }
        
    @property
    def locked(self):
        """Whether the action is locked."""
        return self.workspace.locked()

