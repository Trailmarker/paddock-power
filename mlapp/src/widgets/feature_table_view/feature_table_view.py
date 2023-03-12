# -*- coding: utf-8 -*-
from abc import abstractproperty

from qgis.PyQt.QtCore import QModelIndex, QSize
from qgis.PyQt.QtWidgets import QHeaderView

from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableView

from ...layers.fields import STATUS
from ...models import QtAbstractMeta, WorkspaceMixin
from ...utils import getComponentStyleSheet

from .feature_status_delegate import FeatureStatusDelegate
from .feature_table_action_delegate import FeatureTableActionDelegate
from .feature_table_model import FeatureTableModel
from .feature_table_view_filter_model import FeatureTableViewFilterModel


STYLESHEET = getComponentStyleSheet(__file__)


class FeatureTableView(QgsAttributeTableView, WorkspaceMixin, metaclass=QtAbstractMeta):

    def __init__(self, schema, detailsWidgetFactory=None, editWidgetFactory=None, parent=None):
        QgsAttributeTableView.__init__(self, parent)
        WorkspaceMixin.__init__(self)

        self.setStyleSheet(STYLESHEET)

        self._schema = schema
        self._detailsWidgetFactory = detailsWidgetFactory
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
    def timeframe(self):
        return self.workspace.timeframe

    @property
    def featureLayer(self):
        return self._featureLayer

    @featureLayer.setter
    def featureLayer(self, layer):

        # Clear everything if the new layer is falsy
        if not layer:
            self._featureLayer = None
            self._featureCache = None
            self._tableModel = None
            self._tableFilterModel = None
            self.setModel(None)
            # self.setVisible(False)
            return

        self._featureLayer = layer

        # Wire the feature cache to the feature layer, and the cache to the model
        self._featureCache = QgsVectorLayerCache(self._featureLayer, self._featureLayer.featureCount())
        self._tableModel = FeatureTableModel(
            self._schema,
            self._featureCache,
            self._detailsWidgetFactory,
            self._editWidgetFactory,
            self)

        # Hide the numbers up the left side
        self.verticalHeader().hide()

        # Try to make the columns resize a bit nicer too
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.horizontalHeader().setStretchLastSection(True)
        # self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))

        # Set "whole row only" selection mode
        # self.setSelectionMode(FeatureTableView.SingleSelection)
        self.setSelectionBehavior(FeatureTableView.SelectRows)

        # Load the layer - important that this is prior to setting up the proxy/filter model
        self._tableModel.modelReset.connect(self.onLoadLayer)
        self._featureLayer.editsPersisted.connect(self.onEditsPersisted)
        self._featureLayer.featureDeselected.connect(self.onFeatureDeselected)

        self._tableModel.loadLayer()
        self._tableFilterModel = FeatureTableViewFilterModel(
            self.timeframe, self.plugin.iface.mapCanvas(), self._tableModel, self)
        self.workspace.timeframeChanged.connect(self._tableFilterModel.onTimeframeChanged)
        # Set our model
        self.setModel(self._tableFilterModel)

        self.onLoadLayer()
        self.shrinkToColumns()

        self.show()

    def setFilteredFeatures(self, fids):
        """Filter the table to show only the features with the given FIDs."""
        self._tableFilterModel.setFilteredFeatures(fids)

    def shrinkToColumns(self):
        """Shrink the view down to the minimum size needed to show its columns."""
        self.setVisible(False)
        self.resizeColumnsToContents()
        self.setVisible(True)

        # Get a suitable width for this thing now we've resized the columns
        width = sum(self.horizontalHeader().sectionSize(i) for i in range(self._tableModel.columnCount(QModelIndex())))
        width = width + self.verticalScrollBar().geometry().width()
        self.setMaximumWidth(max(width, self.width()))

    def sizeHint(self):
        hint = super().sizeHint()
        if not self._tableModel:
            return hint
        width = sum(self.horizontalHeader().sectionSize(i) for i in range(self._tableModel.columnCount(QModelIndex())))
        width = width + self.verticalScrollBar().geometry().width()
        return QSize(width, hint.height())

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
                FeatureTableActionDelegate(featureTableActionModel, self))

        # Set up a column item delegate for the "Status" field
        statusColumn = self._tableModel.columnFromFieldName(STATUS)
        if statusColumn >= 0:
            self._statusColumn = statusColumn
            self.setItemDelegateForColumn(self._statusColumn, FeatureStatusDelegate())

        for column in self._tableModel.hiddenColumns:
            self.hideColumn(column)

        # Hide unsupported actions
        for column in range(self._tableModel.featureTableActionCount):
            if column not in [f.value for f in self.supportedFeatureTableActions]:
                self.hideColumn(column)
            else:
                delegate = self.itemDelegateForColumn(column)
                actionModel = delegate.featureTableActionModel
                if not actionModel.isValid:
                    self.hideColumn(column)
            # self.setColumnWidth(column, 100)

    def invalidateCache(self):
        """Invalidate the underlying QgsVectorLayerCache (causes the view to be re-loaded)."""
        self._featureCache.invalidate()

    def indexToFeature(self, index):
        fid = self._tableModel.rowToId(index.row())
        return self._tableModel.layer().getFeature(fid)

    def onTimeframeChanged(self, timeframe):
        """Handle the timeframe being changed."""
        self._tableFilterModel.onTimeframeChanged(timeframe)

    def onEditsPersisted(self):
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
