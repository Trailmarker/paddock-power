# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout

from qgis.utils import iface

from ....utils import PLUGIN_FOLDER, qgsDebug
from .feature_table_action import FeatureTableAction
from .feature_table_action_model import FeatureTableActionModel


class EditFeatureModel(FeatureTableActionModel):
    """A feature table action model that configures editing a feature."""

    _icon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/edit-item.png')

    def __init__(self, editWidgetFactory, parent=None):
        super().__init__(parent)

        self._editWidgetFactory = editWidgetFactory

    def doAction(self, index):
        """Select the feature at the given index."""
        qgsDebug("Edit feature …")

        self.feature = self.getFeature(index)
        dialog = QDialog(iface.mainWindow())
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(self._editWidgetFactory(self.feature))
        dialog.exec_()

    @property
    def featureTableAction(self):
        """The table action associated with this delegate"""
        return FeatureTableAction.editFeature

    def icon(self, _):
        """The icon to paint in the cell."""
        return self._icon

    def description(self, _):
        """The description of the action, given the matching column."""
        return "Edit Feature"
