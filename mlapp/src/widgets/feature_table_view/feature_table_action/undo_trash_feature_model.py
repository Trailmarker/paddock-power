# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ....layers.features import FeatureAction
from ....utils import PLUGIN_FOLDER
from .feature_table_action import FeatureTableAction
from .feature_actions_model import FeatureActionsModel


class UndoTrashFeatureModel(FeatureActionsModel):
    """An item model that rolls back the progress on building, etc, a feature."""

    _trashIcon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/trash-feature.png')
    _undoPlanIcon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/undo-plan-feature.png')
    _undoBuildIcon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/undo-build-feature.png')

    def __init__(self):
        super().__init__()

    @property
    def featureTableAction(self):
        """The table action associated with this delegate"""
        return FeatureTableAction.undoTrashFeature

    @property
    def bumpCacheAfterAction(self):
        """Invalidate the cache after a call to doAction."""
        return True

    @property
    def featureActionIcons(self):
        """A dictionary of FeatureAction objects and their associated icons."""

        return {
            FeatureAction.trash: self._trashIcon,
            FeatureAction.undoPlan: self._undoPlanIcon,
            FeatureAction.undoBuild: self._undoBuildIcon
        }
