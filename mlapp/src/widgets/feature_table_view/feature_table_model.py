# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt

from qgis.gui import QgsAttributeTableModel

from ...utils import PLUGIN_NAME
from .feature_table_action import FeatureTableAction, FeatureTableActionModelFactory


class FeatureTableModel(QgsAttributeTableModel):
    f"""Customisation of the QGIS attribute table model for ${PLUGIN_NAME} features."""

    def __init__(self, displaySchema, featureCache, editWidgetFactory=None):
        super().__init__(featureCache)
        self._displaySchema = displaySchema
        self._tableActionModels = dict(zip(FeatureTableAction, [FeatureTableActionModelFactory(
            editWidgetFactory).createModel(action) for action in FeatureTableAction]))

    @property
    def featureTableActionCount(self):
        """The number of actions in the model."""
        return len(FeatureTableAction)

    @property
    def hiddenColumns(self):
        """Hide columns in the model that are not in the display schema."""

        hiddenColumns = [self.columnFromFieldName(f.name())
                         for f in self.layer().fields()
                         if (f.name() not in self._displaySchema.displayFieldNames())]

        return hiddenColumns

    def columnFromFieldName(self, name):
        """Get the column number for a field in the layer, accounting for the action columns."""
        return self.layer().fields().indexFromName(name) + self.featureTableActionCount

    def rowCount(self, parent):
        """This model has the default row count."""
        return super().rowCount(parent)

    def columnCount(self, parent):
        """This model has the default column count plus the action count."""
        return super().columnCount(parent) + self.featureTableActionCount

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Header data for the action columns is empty."""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section < self.featureTableActionCount:
                return ""
            else:
                return super().headerData(section - self.featureTableActionCount, orientation, role)

    def isToolBarIndex(self, index):
        """Is the index that has been clicked among the action columns?"""
        return index.column() < self.featureTableActionCount

    def data(self, index, role):
        """Get the data at the given index, accounting for the action columns."""
        if self.isToolBarIndex(index):
            featureTableActionModel = self._actionModels[FeatureTableAction(index.column())]

            if role == Qt.DisplayRole:
                return featureTableActionModel.description(index)
            elif role == Qt.ToolTipRole:
                return featureTableActionModel.toolTip(index)
            elif role == Qt.DecorationRole:
                return featureTableActionModel.icon(index)
            else:
                return ""

        return super().data(self.createIndex(index.row(), index.column() - self.featureTableActionCount), role)

    def flags(self, index):
        """Get the flags for the given index, accounting for the action columns."""
        if self.isToolBarIndex(index):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return super().flags(self.createIndex(index.row(), index.column() - self.featureTableActionCount))
