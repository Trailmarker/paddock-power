# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ....utils import PLUGIN_FOLDER
from ...dialogs import DetailsDialog
from .feature_table_action import FeatureTableAction
from .select_feature_model import SelectFeatureModel


class ViewFeatureDetailsModel(SelectFeatureModel):
    """A feature table action model that configures editing a feature."""

    _icon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/view-item.png')

    def __init__(self, detailsWidgetFactory):
        super().__init__()
        self._detailsWidgetFactory = detailsWidgetFactory

    def doAction(self, index):
        """Select the feature at the given index."""
        feature = super().doAction(index)
        if feature:
            detailsDialog = DetailsDialog(feature, self._detailsWidgetFactory, self.plugin.pluginDockWidget)
            detailsDialog.exec_()
        return feature

    @property
    def featureTableAction(self):
        """The table action associated with this delegate"""
        return FeatureTableAction.viewFeatureDetails

    @property
    def isValid(self):
        """Can't use this action without an edit form."""
        return self._detailsWidgetFactory is not None

    @classmethod
    def actionInvalidatesCache(self):
        """Invalidate the cache after a call to doAction."""
        return False

    def icon(self, _):
        """The icon to paint in the cell."""
        return self._icon

    def description(self, _):
        """The description of the action, given the matching column."""
        return "Edit Feature"
