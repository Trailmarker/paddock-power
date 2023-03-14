# -*- coding: utf-8 -*-
from math import floor

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QHBoxLayout, QSplitter, QWidget

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
        self.splitter.setCollapsible(self.splitter.count() - 1, False)

        self.relayout()

    def featureTable(self, index):
        """Get a feature table by index."""
        return self.splitter.widget(index).featureTable

    def setFeatureTableFilteredFeatures(self, index, fids):
        """Set the filtered features of a feature table."""
        self.splitter.widget(index).setFilteredFeatures(fids)

    def setFeatureTableTitle(self, index, title):
        """Set the title of a feature table."""
        self.splitter.widget(index).setTitle(title)

    def setFeatureTableVisible(self, index, visible):
        """Show or hide a feature table."""
        self.splitter.widget(index).setVisible(visible)

    def relayout(self):
        """Get the hint widths of all the splitter items and try to balance them out."""

        hints = [self.splitter.widget(i).sizeHint().width() for i in range(self.splitter.count())]
        neededWidth = sum(hints)
        availableWidth = self.width() - self.splitter.handleWidth() * (self.splitter.count() - 1)
        adjustedSizes = [floor(availableWidth * hint / neededWidth) for hint in hints]
        self.splitter.setSizes(adjustedSizes)
