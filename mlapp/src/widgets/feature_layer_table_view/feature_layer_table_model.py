# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt

from qgis.gui import QgsAttributeTableModel

from ...utils import PLUGIN_FOLDER, qgsDebug


class FeatureLayerTableModel(QgsAttributeTableModel):

    def __init__(self, schema, featureCache):
        QgsAttributeTableModel.__init__(self, featureCache)

        self._schema = schema

    # self.editToolBar.addGenericAction(
    #         f':/plugins/{PLUGIN_FOLDER}/images/zoom-item.png',
    #         f"Zoom to {self.feature.displayName()}",
    #         lambda *_: self.selectFeature())

    # On the left we have:
    # 0. Select
    # 1. Edit
    # 2. Undo or Trash
    # 3. Plan or Build

    @property
    def toolBarCount(self):
        return 4

    @property
    def hiddenColumns(self):
        """Hide columns in the model that are not in the display schema."""

        hiddenColumns = [self.columnIndexFromFieldName(f.name())
                         for f in self.layer().fields()
                         if (f.name() not in self._schema.displayFieldNames())]

        return hiddenColumns

    def columnIndexFromFieldName(self, name):
        return self.layer().fields().indexFromName(name) + self.toolBarCount

    def rowCount(self, parent):
        return super().rowCount(parent)

    def columnCount(self, parent):
        return super().columnCount(parent) + self.toolBarCount

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section < self.toolBarCount:
                return ""
            else:
                return super().headerData(section - self.toolBarCount, orientation, role)

    def isToolBarIndex(self, index):
        return index.column() < self.toolBarCount            

    def data(self, index, role):
        if self.isToolBarIndex(index):

            if role == Qt.DisplayRole:
                return ["Select", "Edit", "Undo or Trash", "Plan or Build"][index.column()]
            elif role == Qt.ToolTipRole:
                return ["Zoom to feature", "Edit feature", "Undo or trash feature", "Plan or build feature"][index.column()]
            else:
                return ""

        return super().data(self.createIndex(index.row(), index.column() - self.toolBarCount), role)
            
    def flags(self, index):
        if self.isToolBarIndex(index):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return super().flags(self.createIndex(index.row(), index.column() - self.toolBarCount))
