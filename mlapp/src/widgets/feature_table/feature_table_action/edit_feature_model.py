# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ....utils import PLUGIN_FOLDER
from ....widgets.dialogs import EditDialog
from .feature_table_action import FeatureTableAction
from .select_feature_model import SelectFeatureModel


class EditFeatureModel(SelectFeatureModel):
    """A feature table action model that configures editing a feature."""

    _icon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/edit-item.png')

    def __init__(self, editWidgetFactory):
        super().__init__()
        self._editWidgetFactory = editWidgetFactory

    def doAction(self, index):
        """Select the feature at the given index."""
        feature = super().doAction(index)
        if feature:
            editDialog = EditDialog(feature, self._editWidgetFactory, self.plugin.pluginDockWidget)
            editDialog.exec_()
        return feature

    @property
    def featureTableAction(self):
        """The table action associated with this delegate"""
        return FeatureTableAction.editFeature

    @property
    def isValid(self):
        """Can't use this action without an edit form."""
        return self._editWidgetFactory is not None

    @property
    def locked(self):
        """Whether the action is locked."""
        return self.workspace.locked()

    def icon(self, _):
        """The icon to paint in the cell."""
        return self._icon

    def description(self, _):
        """The description of the action, given the matching column."""
        return "Edit Feature"
