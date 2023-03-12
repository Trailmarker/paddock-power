# -*- coding: utf-8 -*-
from abc import abstractproperty

from qgis.PyQt.QtCore import Qt

from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableView
from qgis.utils import iface

from ...layers.fields import STATUS
from ...models import QtAbstractMeta, WorkspaceMixin
from ...utils import getComponentStyleSheet, qgsDebug

from .feature_status_delegate import FeatureStatusDelegate
from .feature_table_action import FeatureTableAction
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
        self._statusColumn = None

        self.clicked.connect(self.onClicked)

    def onClicked(self, index):
        if self._tableModel and self._tableModel.isToolBarIndex(index):
            self.onFeatureTableActionClicked(index)

    @abstractproperty
    def supportedFeatureTableActions(self):
        pass

    @property
    def featureLayer(self):
        return self._featureLayer

    @featureLayer.setter
    def featureLayer(self, layer):
        self._featureLayer = layer

        # Wire the feature cache to the feature layer, and the cache to the model
        self._featureCache = QgsVectorLayerCache(self._featureLayer, self._featureLayer.featureCount())
        self._tableModel = FeatureTableModel(self._schema, self._featureCache, self._editWidgetFactory)

        # Hide the numbers up the left side
        self.verticalHeader().hide()

        # Set "whole row only" selection mode
        # self.setSelectionMode(FeatureTableView.SingleSelection)
        self.setSelectionBehavior(FeatureTableView.SelectRows)

        # Load the layer - important that this is prior to setting up the proxy/filter model
        self._tableModel.modelReset.connect(self.onLoadLayer)
        self._featureLayer.editsPersisted.connect(self.onEditsPersisted)
        self._featureLayer.featureDeselected.connect(self.onFeatureDeselected)

        self._tableModel.loadLayer()
        self._tableFilterModel = FeatureTableViewFilterModel(
            self.workspace, self._schema, iface.mapCanvas(), self._tableModel)

        # Set our model
        self.setModel(self._tableFilterModel)

        self.onLoadLayer()
        
        # Weird glitch
        # self.selectRow(-1)
        # self.selectionModel().clearSelection()

        # Resize columns based on contents
        self.setVisible(False)
        self.resizeColumnsToContents()
        self.setVisible(True)

        self.show()

    def onLoadLayer(self):
        """Called when the layer is loaded."""
        config = self.featureLayer.attributeTableConfig()
        columns = config.columns()

        for column in columns:
            if column.name not in self._schema.displayFieldNames():
                column.hidden = True

        config.setColumns(columns)
        self.featureLayer.setAttributeTableConfig(config)

        # Set up column item delegates for all Feature Table Actions
        for featureTableActionModel in self._tableModel.featureTableActionModels:
            self.setItemDelegateForColumn(
                featureTableActionModel.featureTableAction.value,
                FeatureTableActionDelegate(self, featureTableActionModel, self))

        # Set up a column item delegate for the "Status" field
        statusColumn = self._tableModel.columnFromFieldName(STATUS)
        if statusColumn >= 0:
            self._statusColumn = statusColumn
            self.setItemDelegateForColumn(self._statusColumn, FeatureStatusDelegate(self))

        for column in self._tableModel.hiddenColumns:
            self.hideColumn(column)

        # Hide unsupported actions
        for column in range(self._tableModel.featureTableActionCount):
            if column not in [f.value for f in self.supportedFeatureTableActions]:
                self.hideColumn(column)

    def invalidateCache(self):
        """Invalidate the underlying QgsVectorLayerCache (causes the view to be re-loaded)."""
        self._featureCache.invalidate()

    def indexToFeature(self, index):
        fid = self._tableModel.rowToId(index.row())
        return self._tableModel.layer().getFeature(fid)

    def onEditsPersisted(self, edits):
        """Handle a batch of edits being persisted on the underyling layer."""

        # At the moment, we just invalidate the cache and reload the layer
        self.invalidateCache()

    def onFeatureDeselected(self, _):
        """Handle a feature being deselected on the underlying layer."""
        self.selectionModel().clearSelection()
        
    def onFeatureSelected(self, layerId):
        """Handle a feature being selected on the underlying layer."""
        feature = self.workspace.selectedFeature(layerId)  
        if feature:   
            self.selectRow(self._tableModel.idToRow(feature.FID))

    def onFeatureTableActionClicked(self, index):
        """Handle a feature table action being clicked."""
        delegate = self.itemDelegateForColumn(index.column())
        feature = delegate.featureTableActionModel.doAction(index)

        if not feature or delegate.featureTableActionModel.actionInvalidatesCache():
            self.invalidateCache()
