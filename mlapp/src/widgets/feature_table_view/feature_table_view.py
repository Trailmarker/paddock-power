# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableView
from qgis.utils import iface

from ...layers.fields import STATUS
from ...models import QtAbstractMeta, WorkspaceMixin
from ...utils import getComponentStyleSheet, qgsDebug

from .feature_status_delegate import FeatureStatusDelegate
from .feature_table_action_delegate import FeatureTableActionDelegate
from .feature_table_model import FeatureTableModel
from .feature_table_view_filter_model import FeatureTableViewFilterModel


STYLESHEET = getComponentStyleSheet(__file__)


class FeatureTableView(QgsAttributeTableView, WorkspaceMixin, metaclass=QtAbstractMeta):

    def __init__(self, schema, editWidgetFactory=None, parent=None):
        QgsAttributeTableView.__init__(self, parent)
        WorkspaceMixin.__init__(self)

        self.setStyleSheet(STYLESHEET)

        self._schema = schema
        self._editWidgetFactory = editWidgetFactory

        self._featureLayer = None
        self._featureCache = None
        self._tableModel = None
        self._tableFilterModel = None

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
        self._tableModel = FeatureTableModel(self._schema, self._featureCache, self._editWidgetFactory)

        # Set up column item delegates for all Feature Table Actions
        for featureTableActionModel in self._tableModel.featureTableActionModels:
            self.setItemDelegateForColumn(
                featureTableActionModel.featureTableAction.value,
                FeatureTableActionDelegate(featureTableActionModel, self))

        # Set up a column item delegate for the "Status" field
        self.setItemDelegateForColumn(self._tableModel.columnFromFieldName(STATUS), FeatureStatusDelegate(self))

        self._tableModel.modelReset.connect(self.onModelReset)
        self._tableModel.loadLayer()

        self._tableFilterModel = FeatureTableViewFilterModel(
            self.workspace, self._schema, iface.mapCanvas(), self._tableModel)

        self.setModel(self._tableFilterModel)
        self.onModelReset()
        self.show()

    def onModelReset(self):
        """Hide columns in the table that are not in the display schema."""
        # Hide the numbers up the left side
        self.verticalHeader().hide()

        for column in self._tableModel.hiddenColumns:
            self.hideColumn(column)

        self.setVisible(False)
        self.resizeColumnsToContents()
        self.setVisible(True)

    def indexToFeature(self, index):
        fid = self._tableModel.rowToId(index.row())
        return self._tableModel.layer().getFeature(fid)

    def onToolBarClicked(self, index):
        delegate = self.itemDelegateForColumn(index.column())
        featureTableActionModel = delegate.featureTableActionModel
        featureTableActionModel.doAction(index)
        
        if featureTableActionModel.bumpCacheAfterAction:
            self.bumpCache()
            
    def bumpCache(self):
        """Bump the cache."""
        qgsDebug(f"{type(self).__name__}.bumpCache()")
        if self._featureCache:
            # Re-cache all the data
            self._tableModel.resetModel()
            self._featureCache.setFullCache(True)
