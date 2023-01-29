# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QFrame, QListWidget, QListWidgetItem, QSizePolicy

from ...spatial.layers.mixins.workspace_connection_mixin import WorkspaceConnectionMixin
from ...utils import qgsDebug


class FeatureListBase(QListWidget, WorkspaceConnectionMixin):

    @classmethod
    def getFeatureType(cls):
        raise NotImplementedError

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
                           in widget.feature.NAME.lower())

    def getFeatures():
        """Get the Features."""
        raise NotImplementedError("getFeatures() must be implemented in a subclass")


    def refreshUi(self):
        """Show the Feature List."""
        # Initially clear the list
        self.clear()

        features = self.getFeatures()

        if not features:
            return

        # Sort Features alphabetically
        features.sort(key=lambda x: x.NAME)

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


    # Overriding default WorkspaceMixin behaviour
    def removeSelection(self):
        """Clear the selected Feature."""
        qgsDebug(f"Clearing selection in {self.__class__.__name__}")
        self.clearSelection()
    
    # Overriding default WorkspaceMixin behaviour
    def changeSelection(self, feature):
        """Select the Feature."""
        self.removeSelection()
        if feature:
            qgsDebug(f"Selecting Feature {feature.id} in {self.__class__.__name__}")
            for item in [self.item(i) for i in range(self.count())]:
                widget = self.itemWidget(item)
                if widget.feature.FID == feature.id():  # TODO might this lead to "old" copies of the Feature "aliasing"?
                    self.setCurrentItem(item)
                    return
