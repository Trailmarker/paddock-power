# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ....utils import PLUGIN_FOLDER
from .feature_table_action import FeatureTableAction
from .feature_table_action_model import FeatureTableActionModel


class SelectFeatureModel(FeatureTableActionModel):
    """A feature table action model that configures selecting a feature."""

    _icon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/zoom-item.png')

    def __init__(self, parent=None):
        super().__init__(parent)

    def doAction(self, index):
        """Select the feature at the given index."""
        feature = self.getFeature(index)
        feature.selectFeature()

    @property
    def featureTableAction(self):
        """The table action associated with this model."""
        return FeatureTableAction.selectFeature

    def icon(self, index):
        """The icon to paint in the cell."""
        return self._icon

    def description(self, index):
        """The description of the action."""
        return "Select Feature"
