# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QFrame, QListWidget, QListWidgetItem

from .paddock_collapsible_list_item import PaddockCollapsibleListItem


class PaddockListBase(QListWidget):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(parent)
        # self.setWidgetResizable(True)
        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSizeAdjustPolicy(QListWidget.AdjustToContents)

    def filterByName(self, filter):
        """Filter the paddock list by name."""
        for item in [self.item(i) for i in range(self.count())]:
            widget = self.itemWidget(item)
            item.setHidden(not filter in str(widget.paddock["Paddock Name"]))

    def getPaddocks():
        """Get the paddocks."""
        raise NotImplementedError(
            "getPaddocks() must be implemented in a subclass")

    def refreshUi(self):
        """Show the Paddock List."""
        paddocks = self.getPaddocks()

        # Sort Paddocks alphabetically
        paddocks.sort(key=lambda x: x["Paddock Name"])

        # Initially clear the list
        self.clear()

        # Then repopulate it if we have Paddocks
        if paddocks is not None:
            for paddock in paddocks:
                widget = PaddockCollapsibleListItem(paddock)
                item = QListWidgetItem(self)
                item.setSizeHint(widget.sizeHint())

                # Prevent selection of the items
                item.setFlags(item.flags() | Qt.ItemIsSelectable)

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
        hint.setWidth(self.sizeHintForColumn(0) + self.verticalScrollBar().width())

        return hint
