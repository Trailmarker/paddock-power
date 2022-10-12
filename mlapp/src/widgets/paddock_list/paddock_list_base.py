# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QListWidget, QListWidgetItem

from .paddock_collapsible_list_item import PaddockCollapsibleListItem

class PaddockListBase(QListWidget):
    refreshUiNeeded = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""

        super(QListWidget, self).__init__(parent)
        self.setSizeAdjustPolicy(QListWidget.AdjustToContents)

    def filterByName(self, filter):
        """Filter the paddock list by name."""
        for item in [self.item(i) for i in range(self.count())]:
            widget = self.itemWidget(item)
            item.setHidden(not filter in widget.paddock["Paddock Name"])

    def getPaddocks():
        """Get the paddocks."""
        raise NotImplementedError("getPaddocks() must be implemented in a subclass")

    def refreshUi(self):
        """Show the Paddock List."""
        paddocks = self.getPaddocks()

        if paddocks is not None:
            for paddock in paddocks:
                widget = PaddockCollapsibleListItem(paddock)
                item = QListWidgetItem(self)
                item.setSizeHint(widget.sizeHint())
                self.addItem(item)
                self.setItemWidget(item, widget)
                widget.collapsed.connect(self.refreshLayout)
                widget.expanded.connect(self.refreshLayout)
        else:
            self.clear()

    def refreshLayout(self):
        """Refresh the layout based on the size hints of all the custom widgets."""
        for item in [self.item(i) for i in range(self.count())]:
            item.setSizeHint(self.itemWidget(item).sizeHint())