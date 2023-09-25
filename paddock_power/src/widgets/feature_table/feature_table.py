# -*- coding: utf-8 -*-
from abc import abstractproperty

from qgis.PyQt.QtCore import QSize, Qt
from qgis.PyQt.QtWidgets import QHeaderView, QSizePolicy

from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableView

from ...layers.fields import ANALYSIS_TYPE, CONDITION_TYPE, STATUS, AnalysisType, ConditionType, FeatureStatus
from ...models import WorkspaceMixin
from ...utils import PLUGIN_NAME, getComponentStyleSheet, guiWarning

from .. import RelayoutMixin
from ..delegates.field_domain_delegate import FieldDomainDelegate
from .feature_table_action_delegate import FeatureTableActionDelegate
from .feature_table_model import FeatureTableModel
from .feature_table_filter_model import FeatureTableFilterModel


STYLESHEET = getComponentStyleSheet(__file__)


class FeatureTable(RelayoutMixin, WorkspaceMixin, QgsAttributeTableView):

    UNIT = 10
    PADDING = 5 * UNIT

    def __init__(self, schema, detailsWidgetFactory=None, editWidgetFactory=None, parent=None):
        RelayoutMixin.__init__(self)
        WorkspaceMixin.__init__(self)
        QgsAttributeTableView.__init__(self, parent)

        # Used to configure the filter model 'display mode'
        self.displayMode = False

        # Used to configure the table model in line with the plugin's domain
        self._schema = schema
        self._detailsWidgetFactory = detailsWidgetFactory
        self._editWidgetFactory = editWidgetFactory

        # Qt's extensive plumbing for the feature table
        self._featureLayer = None
        self._featureCache = None
        self._tableModel = None
        self._tableFilterModel = None

        # Stash some data about the columns we load for laying out the widget
        self._columnMetrics = None

        self.clicked.connect(self.onClicked)

        # Base appearance
        self.setStyleSheet(STYLESHEET)

        # Hide QGIS's default row numbers up the left side
        self.verticalHeader().hide()

        # Allow the table to be reduced in width and height, but also make it use what it gets
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # The section sizes in the table are handled in self.relayout below
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.horizontalHeader().setStretchLastSection(True)

        self.setWordWrap(False)

        # Set "whole row only" selection mode
        self.setSelectionMode(FeatureTable.SingleSelection)
        self.setSelectionBehavior(FeatureTable.SelectRows)

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
            self.setVisible(False)
            self.clearFeatureLayer()
            return

        # Set the new layer
        self._featureLayer = layer
        self._featureLayer.willBeDeleted.connect(self.clearFeatureLayer)

        # Wire the feature cache to the feature layer, and the cache to the model
        self._featureCache = QgsVectorLayerCache(self._featureLayer, self._featureLayer.featureCount())
        self._tableModel = FeatureTableModel(
            self._schema,
            self._featureCache,
            self._detailsWidgetFactory,
            self._editWidgetFactory,
            self)

        # Load the layer - important that this is prior to setting up the proxy/filter model
        self._tableModel.modelReset.connect(self.onFeatureLayerLoaded)

        # Persisting edits will invalidate the cache
        # self._featureLayer.editsPersisted.connect(self.onEditsPersisted)

        # Selecting a feature will scroll to that feature in the table if it's not visible
        self.workspace.featureSelected.connect(self.onFeatureSelected)

        self._tableModel.loadLayer()
        self._tableFilterModel = FeatureTableFilterModel(
            self.timeframe, self.plugin.iface.mapCanvas(), self._tableModel, self)

        # Apply the 'display mode' to the filter model if set
        self._tableFilterModel.displayMode = self.displayMode

        self.setSortingEnabled(True)
        self.sortByColumn(self._tableModel.sortColumn, Qt.AscendingOrder)

        self.workspace.timeframeChanged.connect(self._tableFilterModel.onTimeframeChanged)
        self.workspace.lockChanged.connect(self.onLockChanged)

        # Set our model
        self.setModel(self._tableFilterModel)

        self.onFeatureLayerLoaded()

    def clearFeatureLayer(self):
        # Clear everything if the new layer is falsy
        self.setModel(None)
        self._tableFilterModel = None
        self._tableModel = None
        self._featureCache = None
        self._featureLayer = None

        return

    def setFilteredFeatures(self, fids):
        """Filter the table to show only the features with the given FIDs."""
        self._tableFilterModel.setFilteredFeatures(fids)

    def relayout(self):
        """Shrink the view down to the minimum size needed to show its columns."""

        # We don't do this algebra when no one's looking
        if not self.isVisible():
            return

        if not self._columnMetrics:
            return

        (padding, baseSectionSizes, sectionsToResize) = self._columnMetrics

        scrollBarWidth = self.verticalScrollBar().geometry().width()  # if self.verticalScrollBar().isVisible() else 0

        neededWidth = sum(baseSectionSizes) + scrollBarWidth
        preferredWidth = neededWidth + len(sectionsToResize) * padding

        # If we have our preferred width available within our parent, expand into it
        # if preferredWidth < (self.parent().width() - 6) and self.width() < preferredWidth:
        #     self.resize(preferredWidth, self.height())
        #     return

        for i in sectionsToResize:
            self.horizontalHeader().resizeSection(
                i, baseSectionSizes[i])

        # Section change can be negative? Nah …
        # sectionIncrease = min(max(self.width() - neededWidth, 0) // len(sectionsToResize), padding)
        # fineModulus = 0 if sectionIncrease >= padding else (max(self.width() - neededWidth, 0) % len(sectionsToResize))

        # for i in sectionsToResize:
        #     self.horizontalHeader().resizeSection(
        #         i, baseSectionSizes[i] + sectionIncrease + (1 if i < fineModulus else 0))

    def sizeHint(self):
        hint = super().sizeHint()

        if not self._columnMetrics:
            self._columnMetrics = self.updateColumnMetrics()

        (padding, baseSectionSizes, sectionsToResize) = self._columnMetrics

        scrollBarWidth = self.verticalScrollBar().geometry().width()  # if self.verticalScrollBar().isVisible() else 0

        neededWidth = sum(baseSectionSizes) + scrollBarWidth

        return QSize(neededWidth, hint.height())

    def setFeatureFieldDomainDelegate(self, fieldName, fieldDomainType):
        """Set up a column item delegate for the given field name and domain type."""
        column = self._tableModel.columnFromFieldName(fieldName)
        if column >= 0:
            self.setItemDelegateForColumn(column, FieldDomainDelegate(fieldDomainType, self))

    def onFeatureLayerLoaded(self):
        """Called when the layer is loaded."""
        config = self.featureLayer.attributeTableConfig()
        columns = config.columns()

        for column in columns:
            if column.name in self._schema.hiddenFieldNames():
                column.hidden = True

        config.setColumns(columns)
        self.featureLayer.setAttributeTableConfig(config)

        # Set up column item delegates for all Feature Table Actions
        for featureTableActionModel in self._tableModel.featureTableActionModels:
            self.setItemDelegateForColumn(
                featureTableActionModel.featureTableAction.value,
                FeatureTableActionDelegate(featureTableActionModel, self))

        # Set up a column item delegate for the "Analysis Type", "Condition Type" and "Status" fields
        self.setFeatureFieldDomainDelegate(ANALYSIS_TYPE, AnalysisType)
        self.setFeatureFieldDomainDelegate(CONDITION_TYPE, ConditionType)
        self.setFeatureFieldDomainDelegate(STATUS, FeatureStatus)

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

        self.updateColumnMetrics()
        self.setVisible(True)
        self.show()

    def updateColumnMetrics(self):

        # First resize all columns to their contents, nice and snug
        self.setVisible(False)
        self.resizeColumnsToContents()
        self.setVisible(True)

        # Preferred section padding
        padding = self.PADDING

        # Figure out the metrics of our resized columns
        header = self.horizontalHeader()
        baseSectionSizes = [header.sectionSize(i) for i in range(header.count())]

        # Allow all our columns except the action buttons to grow
        sectionsToResize = [
            i for i in range(
                self._tableModel.featureTableActionCount if self._tableModel else 0,
                header.count()) if header.sectionSize(i) > 0]

        self._columnMetrics = (padding, baseSectionSizes, sectionsToResize)
        return self._columnMetrics

    def invalidateCache(self):
        """Invalidate the underlying QgsVectorLayerCache (causes the view to be re-loaded)."""
        if self._featureCache:
            self._featureCache.invalidate()

    def indexToFeature(self, index):
        fid = self._tableModel.rowToId(index.row())
        return self._tableModel.layer().getFeature(fid)

    def onTimeframeChanged(self):
        """Handle the timeframe being changed."""
        self._tableFilterModel.onTimeframeChanged()

    # def onEditsPersisted(self):
    #     """Handle a batch of edits being persisted on the underyling layer."""
    #     # At the moment, we just invalidate the cache and reload the layer
    #     self.invalidateCache()

    def hasLayerId(self, layerId):
        """Return True if this FeatureTable is built on a FeatureLayer with a matching layer ID."""
        return self.featureLayer and self.featureLayer.id() == layerId

    def onFeatureSelected(self, layerId):
        """Scroll to new selection when feature selected, if not visible."""
        if not self.hasLayerId(layerId):
            return

        feature = self.workspace.selectedFeature(layerId)
        if feature:
            row = self._tableModel.idToRow(feature.FID)
            if row and row >= 0:
                self.scrollTo(self.model().index(row, 0))

    def onFeatureTableActionClicked(self, index):
        """Handle a feature table action being clicked."""
        delegate = self.itemDelegateForColumn(index.column())

        if not delegate or not delegate.featureTableActionModel:
            return

        if delegate.featureTableActionModel.locked:
            guiWarning(f"Please wait while {PLUGIN_NAME} finishes processing.")
        else:
            delegate.featureTableActionModel.doAction(index)

    def onLockChanged(self, locked):
        """Handle the lock state changing."""

        # When the workspace is unlocked, we assume data may have changed and reload our cache
        if not locked:
            self.invalidateCache()
