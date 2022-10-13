# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QFrame, QListWidget, QListWidgetItem

from ...models.paddock_power_state import PaddockPowerState
from .fence_list_item import FenceListItem

class FenceList(QListWidget):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSizeAdjustPolicy(QListWidget.AdjustToContents)

        self.setMaximumWidth(500)

        self.state = PaddockPowerState()
        self.state.milestoneChanged.connect(self.refreshUi)

        self.refreshUi()

    def getFences(self):
        """Get the fences."""
        milestone = self.state.getMilestone()
        return [fence for fence in milestone.fenceLayer.getFeatures()] if milestone is not None else None

    def refreshUi(self):
        """Show the Paddock List."""
        # Initially clear the list
        self.clear()

        fences = self.getFences()

        if not fences:
            self.setVisible(False)
            return

        self.setVisible(True)   

        # Sort Fences by Build Order
        fences.sort(key=lambda x: x.fenceBuildOrder())

        # Repopulate list if we have Fences
        for fence in fences:
            widget = FenceListItem(fence)
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
        hint.setWidth(self.sizeHintForColumn(0) + self.verticalScrollBar().width())

        return hint
