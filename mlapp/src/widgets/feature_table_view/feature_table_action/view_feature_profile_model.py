# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ....utils import PLUGIN_FOLDER
from ....widgets.profile_details.profile_details_dialog import ProfileDetailsDialog
from .feature_table_action import FeatureTableAction
from .feature_table_action_model import FeatureTableActionModel


class ViewFeatureProfileModel(FeatureTableActionModel):
    """A feature table action model that configures viewing the profile of a feature."""

    _icon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/elevation.png')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.profileDetailsDialog = None

    def doAction(self, index):
        """View the profile for the feature at the given index."""
        self.feature = self.getFeature(index)
        
        if not self.profileDetailsDialog:
            self.profileDetailsDialog = ProfileDetailsDialog(self.feature, self)

        self.profileDetailsDialog.show()

    @property
    def featureTableAction(self):
        """The table action associated with this model."""
        return FeatureTableAction.viewFeatureProfile

    def icon(self, _):
        """The icon to paint in the cell."""
        return self._icon

    def description(self, _):
        """The description of the action."""
        return "Show Elevation Profile"
