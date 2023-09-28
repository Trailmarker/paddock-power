# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ....models import WorkspaceMixin
from ....utils import PLUGIN_FOLDER, PLUGIN_NAME, guiWarning
from ....widgets import ProfileDetailsDialog
from .feature_table_action import FeatureTableAction
from .feature_table_action_model import FeatureTableActionModel


class ViewFeatureProfileModel(FeatureTableActionModel, WorkspaceMixin):
    """A feature table action model that configures viewing the profile of a feature."""

    _icon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/elevation.png')

    def __init__(self):
        super().__init__()
        self.profileDetailsDialog = None

    def doAction(self, index):
        """View the profile for the feature at the given index."""
        feature = self.getFeature(index)
        hasElevation = self.workspace.hasElevation

        if not hasElevation:
            guiWarning(
                f"No elevation profile can be shown: there is no valid elevation data in your {PLUGIN_NAME} workspace.")

        if feature and hasElevation:
            # Not iface.mainWindow() as it messed with the styles
            profileDetailsDialog = ProfileDetailsDialog(feature, self.plugin.pluginDockWidget)
            profileDetailsDialog.show()

        return feature

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
