# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from qgis.PyQt.QtWidgets import QDialog, QTableView, QVBoxLayout

from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableView
from qgis.utils import iface

from ...models import QtAbstractMeta, WorkspaceMixin
from ...utils import PLUGIN_FOLDER, getComponentStyleSheet, qgsDebug

from .feature_layer_table_model import FeatureLayerTableModel
from .feature_layer_table_view_filter_model import FeatureLayerTableViewFilterModel
from .feature_icon_delegate import FeatureIconDelegate

from ..paddock_details.paddock_details_edit import PaddockDetailsEdit


STYLESHEET = getComponentStyleSheet(__file__)


class FeatureLayerTableView(QgsAttributeTableView, WorkspaceMixin, metaclass=QtAbstractMeta):

    def __init__(self, schema, editWidgetFactory, parent=None):
        QgsAttributeTableView.__init__(self, parent)
        WorkspaceMixin.__init__(self)

        self.setStyleSheet(STYLESHEET)

        self._schema = schema
        self._editWidgetFactory = editWidgetFactory

        self._featureLayer = None
        self._featureCache = None
        self._tableModel = None
        self._tableFilterModel = None

        self._selectDelegate = FeatureIconDelegate(QIcon(f':/plugins/{PLUGIN_FOLDER}/images/zoom-item.png'))
        self._editDelegate = FeatureIconDelegate(QIcon(f':/plugins/{PLUGIN_FOLDER}/images/edit-item.png'))

        self.setItemDelegateForColumn(0, self._selectDelegate)
        self.setItemDelegateForColumn(1, self._editDelegate)

        self.clicked.connect(self.onClicked)

    def onClicked(self, index):
        qgsDebug(f"Received click at index {index.row()}, {index.column()}")
        if self._tableModel.isToolBarIndex(index):
            self.onToolBarClicked(index)

    @property
    def featureLayer(self):
        return self._featureLayer

    @featureLayer.setter
    def featureLayer(self, layer):
        self._featureLayer = layer

        config = self._featureLayer.attributeTableConfig()
        columns = config.columns()

        for column in columns:
            if column.name not in self._schema.displayFieldNames():
                qgsDebug(f"Hiding column {column.name}")
                column.hidden = True

        config.setColumns(columns)
        self._featureLayer.setAttributeTableConfig(config)

        self._featureCache = QgsVectorLayerCache(layer, layer.featureCount())
        # self._tableModel = QgsAttributeTableModel(self._featureCache)
        self._tableModel = FeatureLayerTableModel(self._schema, self._featureCache)
        self._tableModel.modelReset.connect(self.onModelReset)
        self._tableModel.loadLayer()

        # self._tableFilterModel = QgsAttributeTableFilterModel(iface.mapCanvas(), self._tableModel)
        self._tableFilterModel = FeatureLayerTableViewFilterModel(
            self.workspace, self._schema, iface.mapCanvas(), self._tableModel)

        self.setModel(self._tableFilterModel)
        self.onModelReset()
        self.show()

    def onModelReset(self):
        """Hide columns in the table that are not in the display schema."""

        for column in self._tableModel.hiddenColumns:
            self.hideColumn(column)

        for column in range(self._tableModel.toolBarCount):
            self.setColumnWidth(column, 30)

    def viewRowToFeature(self, index):
        fid = self._tableModel.rowToId(index.row())
        return self._tableModel.layer().getFeature(fid)


    def onToolBarClicked(self, index):
        feature = self.viewRowToFeature(index)

        if index.column() == 0:
            self.selectFeature(index, feature)
        elif index.column() == 1:
            self.editFeature(index, feature)
        elif index.column() == 2:
            qgsDebug(f"Undo or trash {feature}")
        elif index.column() == 3:
            qgsDebug(f"Build or plan {feature}")

    def selectFeature(self, index, feature):
        feature.selectFeature()

    def editFeature(self, index, feature):
        qgsDebug(f"Edit feature {feature}")

        dialog = QDialog(iface.mainWindow())
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(self._editWidgetFactory(feature))

        dialog.exec_()
