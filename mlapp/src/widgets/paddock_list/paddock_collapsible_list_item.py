# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QSize
from qgis.PyQt.QtWidgets import QVBoxLayout, QWidget

from ..collapse.collapse import Collapse
from ..paddock_details.paddock_details import PaddockDetails


class PaddockCollapsibleListItem(QWidget):
    collapsed = pyqtSignal()
    expanded = pyqtSignal()

    def __init__(self, paddock, parent=None):
        super(QWidget, self).__init__(parent)

        self.paddock = paddock
        paddockDetails = PaddockDetails(paddock)

        collapseLayout = QVBoxLayout()
        collapseLayout.setSpacing(0)
        collapseLayout.setContentsMargins(0, 0, 0, 0)
        collapseLayout.addWidget(paddockDetails)
        collapseLayout.addStretch()

        self.collapse = Collapse(self)
        self.collapse.setContentLayout(collapseLayout)

        self.setTitle(str(paddock["Paddock Name"]))

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.collapse)
        layout.addStretch()

        self.setLayout(layout)

        self.collapse.collapsed.connect(self.collapsed.emit)
        self.collapse.expanded.connect(self.expanded.emit)

    def setTitle(self, title):
        self.collapse.setTitle(title)

    def sizeHint(self):
        """Return the size of the widget."""
        hint = QSize(self.collapse.sizeHint().width(),
                     self.collapse.sizeHint().height())
        return hint
