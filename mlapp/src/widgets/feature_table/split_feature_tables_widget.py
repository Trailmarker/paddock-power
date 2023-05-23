# -*- coding: utf-8 -*-
from math import floor

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QHBoxLayout, QSplitter, QWidget

from ...utils import qgsDebug
from ..relayout_mixin import RelayoutMixin
from .feature_table_group_box import FeatureTableGroupBox


class SplitFeatureTablesWidget(RelayoutMixin, QWidget):
    """A widget that displays adjacent (and possibly interacting) feature tables."""

    def __init__(self, parent=None):
        """Set up the container then use addFeatureTable to add the feature tables."""
        RelayoutMixin.__init__(self)
        QWidget.__init__(self, parent)

        self.horizontalLayout = QHBoxLayout(self)
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.horizontalLayout.addWidget(self.splitter)
        self.horizontalLayout.addStretch()
        self.setLayout(self.horizontalLayout)

    def addFeatureTable(self, title, featureTableFactory, popupLayerTypes=None, popupLayerSource=None, visible=True):
        """Adds a feature table to the splitter."""
        groupBox = FeatureTableGroupBox()
        groupBox.setTitle(title)
        groupBox.featureTableFactory = featureTableFactory
        if popupLayerTypes is not None:
            groupBox.popupLayerTypes = popupLayerTypes
        if popupLayerSource is not None:
            groupBox.popupLayerSource = popupLayerSource

        groupBox.setVisible(visible)
        self.splitter.addWidget(groupBox)

        self.relayout()

    def featureTable(self, index):
        """Get a feature table by index."""
        return self.splitter.widget(index).featureTable

    def hasLayerId(self, layerId):
        """Return True if one of the FeatureTables held in this splitter has a matching layer ID."""
        return any(self.featureTable(i) and self.featureTable(i).hasLayerId(layerId)
                   for i in range(self.splitter.count()))

    def setFeatureTableFilteredFeatures(self, index, fids):
        """Set the filtered features of a feature table."""
        self.featureTable(index).setFilteredFeatures(fids)

    def setFeatureTableTitle(self, index, title):
        """Set the title of a feature table."""
        self.splitter.widget(index).setTitle(title)

    def setFeatureTableVisible(self, index, visible):
        """Show or hide a feature table."""
        self.splitter.widget(index).setVisible(visible)

    def hideEvent(self, event):
        """Re-lay out when the widget is hidden."""
        self.relayout()
        super().hideEvent(event)

    def showEvent(self, event):
        """Re-lay out when the widget is shown."""
        self.relayout()
        super().showEvent(event)

    def relayout(self):
        """Get the hint widths of all the splitter items and try to balance them out."""
        count = self.splitter.count()
        sizes = [self.splitter.widget(i).width() for i in range(count)]
        hints = [self.splitter.widget(i).sizeHint().width() for i in range(count)]

        # qgsDebug(f"SplitFeatureTablesWidget.relayout: sizes = {sizes}, hints = {hints}")

        available = self.width() - self.splitter.handleWidth() * (count - 1)
        current = sum(sizes)
        needed = sum(hints)

        # qgsDebug(f"SplitFeatureTablesWidget.relayout: available = {available}, current = {current}, needed = {needed}")

        # If we have room, try to make everything at least the hint
        if needed <= available and current < available:
            sizes = [max(hint, size) for (hint, size) in zip(hints, sizes)]
        # Or at least let's get the first item
        elif hints[0] <= available:
            sizes[0] = hints[0]

        current = sum(sizes)
        # qgsDebug(f"SplitFeatureTablesWidget.relayout: after expanding, sizes = {sizes}, current = {current}, available = {available}")

        # If we've got too much, bring everything down to the hint at maximum,
        # shrinking from the right first
        for i in reversed(range(count)):
            if current <= available:
                break
            elif sizes[i] > hints[i]:
                sizes[i] = hints[i]
                current = sum(sizes)

        # qgsDebug(f"SplitFeatureTablesWidget.relayout: after shrinking from the right, sizes = {sizes}, current = {current}, available = {available}")

        # If we've still got too much, accept that we're going to have to shrink,
        # but favour the first item
        first = hints[0]

        if current > available and first <= available:

            (tneed, tavail) = (sum(hints[1:]), available - first)
            sizes = [first] + [(tavail * hint) // tneed for hint in hints[1:]]

        current = sum(sizes)

        # qgsDebug(f"SplitFeatureTablesWidget.relayout: after forced shrink, sizes = {sizes}, current = {current}, available = {available}")

        # If we've still got too much, squash the first item too
        if current > available:
            sizes = [max(sizes[0] - (current - available), 0)] + [0 for s in sizes[1:]]

        # qgsDebug(f"SplitFeatureTablesWidget.relayout: after final shrink, sizes = {sizes}, current = {current}")

        self.splitter.setSizes(sizes)
