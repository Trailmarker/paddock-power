# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import QFrame, QListWidget, QListWidgetItem, QSizePolicy

from ...spatial.features.feature import Feature
from ...utils import qgsDebug


class FeatureListBase(QListWidget):

    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.listItemFactory = listItemFactory

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
                           in widget.feature.name.lower())

    def getFeatures():
        """Get the Features."""
        raise NotImplementedError("getFeatures() must be implemented in a subclass")

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, feature):
        """Select the Feature."""
        self.clearSelection()
        if feature:
            # qgsDebug(f"Selecting Feature {feature.id} in {self.__class__.__name__}")
            for item in [self.item(i) for i in range(self.count())]:
                widget = self.itemWidget(item)
                if widget.feature.FID == feature.FID:  # TODO might this lead to "old" copies of the Feature "aliasing"?
                    self.setCurrentItem(item)
                    return

    def refreshUi(self):
        """Show the Feature List."""
        # Initially clear the list
        self.clear()

        features = self.getFeatures()

        if not features:
            return

        # Sort Features alphabetically
        features.sort(key=lambda x: x.name)

        # Repopulate list since we have Features
        for feature in features:
            widget = self.listItemFactory(feature)
            item = QListWidgetItem(self)
            item.setSizeHint(widget.sizeHint())

            # Prevent selection of the items
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

            self.addItem(item)
            self.setItemWidget(item, widget)

            widget.layoutRefreshNeeded.connect(self.refreshLayout)

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
