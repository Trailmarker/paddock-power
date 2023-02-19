# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView, QFrame, QListWidget, QListWidgetItem, QSizePolicy


from ...models import WorkspaceMixin
from ...utils import qgsDebug


class FeatureListBase(QListWidget, WorkspaceMixin):

    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        QListWidget.__init__(self, parent)
        WorkspaceMixin.__init__(self)

        self._selectedFeature = None
        self._selectedItem = None
        self._listItemFactory = listItemFactory

        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSizeAdjustPolicy(QListWidget.AdjustToContents)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

    def filterByName(self, filter):
        """Filter the Feature list by name."""
        if filter is None:
            return
        for item in [self.item(i) for i in range(self.count())]:
            widget = self.itemWidget(item)
            item.setHidden(not filter.lower()
                           in widget.feature.NAME.lower())

    def getFeatures():
        """Get the Features."""
        raise NotImplementedError("getFeatures() must be implemented in a subclass")

    def sortFeatures(self, features):
        """Sort the Features."""
        features.sort(key=lambda x: x.NAME)
        return features

    def deduplicateFeatures(self, features):
        """De-duplicate the Features. May be necessary to provide this for some FeatureLayerList subclasses."""
        return features

    def refreshUi(self):
        """Show the Feature List."""

        # qgsDebug(f"{type(self).__name__}.refreshUi()")

        # Initially clear the list
        self.clear()
        self.removeSelection()

        features = self.getFeatures()

        # De-duplicate Features
        features = self.deduplicateFeatures(features)

        # Sort Features alphabetically
        features = self.sortFeatures(features)

        # Repopulate list since we have Features
        for feature in features:
            widget = self._listItemFactory(feature)
            item = QListWidgetItem(self)
            item.setSizeHint(widget.sizeHint())

            # Prevent selection of the items
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

            self.addItem(item)
            self.setItemWidget(item, widget)

            if self._selectedFeature and self._selectedFeature.FID == feature.FID:
                self._selectedItem = item
                # qgsDebug(f"{type(self).__name__}.refreshUi(): selectedItem = {feature}")
            widget.layoutRefreshNeeded.connect(self.refreshLayout)

        if self._selectedItem:
            self.itemWidget(self._selectedItem).setSelected(True)
            self.scrollToItem(self._selectedItem, QAbstractItemView.PositionAtTop)

    def refreshLayout(self):
        """Refresh the layout based on the size hints of all the custom widgets."""
        for item in [self.item(i) for i in range(self.count())]:
            item.setSizeHint(self.itemWidget(item).sizeHint())

    def sizeHint(self):
        hint = super().sizeHint()

        # Add the width of the vertical scrollbar
        hint.setWidth(self.sizeHintForColumn(
            0) + self.verticalScrollBar().width())

        return hint

    def removeSelection(self):
        """Clear the selected Feature."""
        # if self._selectedItem:
        #     self.itemWidget(self._selectedItem).setSelected(False)
        self._selectedItem = None
        self.clearSelection()

    def changeSelection(self, layerType):
        """Select the Feature."""
        self._selectedFeature = self.workspace.selectedFeature(layerType)
        self.refreshUi()
