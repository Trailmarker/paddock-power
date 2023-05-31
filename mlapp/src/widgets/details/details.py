# -*- coding: utf-8 -*-
from enum import Enum
from functools import cached_property

from qgis.PyQt.QtCore import QSize, Qt
from qgis.PyQt.QtWidgets import QGridLayout, QLabel, QSizePolicy, QToolBar, QWidget

from .formatted_values import FormattedValues


class Details(QWidget):

    class DisplayMode(Enum):
        Central = "Align labels and details around the central axis"
        Outer = "Align labels and details around the left and right perimeters"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.gridLayout = QGridLayout(self)
        # self.gridLayout.setSpacing(6)
        # self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.toolBar = QToolBar(self)
        self.toolBar.setContentsMargins(0, 0, 0, 0)
        self.toolBar.setOrientation(Qt.Vertical)

        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        self._model = None
        self._inverted = False
        self._displayMode = Details.DisplayMode.Central

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model
        self.refreshUi()

    @property
    def descriptors(self):
        """Return the formatting for the details."""
        return []

    @property
    def inverted(self):
        """Return if this widget is inverted."""
        return self._inverted

    @inverted.setter
    def inverted(self, inverted):
        """Set the inverted state for the details."""
        self._inverted = inverted
        self.refreshUi()

    @property
    def displayMode(self):
        """Return the size hint for the details."""
        return self._displayMode

    @displayMode.setter
    def displayMode(self, mode):
        """Set the inverted state for the details."""
        self._displayMode = mode
        self.refreshUi()

    def label(self, descriptor):
        (_, label, _) = descriptor
        obj = QLabel(label)
        font = obj.font()
        font.setBold(True)
        obj.setFont(font)
        return obj

    def valueFormatter(self, descriptor):
        (extractor, _, formatSpec) = descriptor
        return lambda m: FormattedValues().setValues(formatSpec, *extractor(m))

    @cached_property
    def labels(self):
        return [self.label(d) for d in self.descriptors]

    def addAction(self, action):
        """Add an action to the Details widget's toolbar."""
        self.toolBar.addAction(action)
        self.refreshUi()

    def refreshUi(self):
        """Refresh the details UI."""

        detailsCount = len(self.descriptors)

        # Try to get any current items in the grid layout and remove them
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.removeWidget(self.gridLayout.itemAt(i).widget())

        if self.model is not None:
            # If there are any actions, add our toolbar
            if self.toolBar.actions():
                self.gridLayout.addWidget(self.toolBar, 0, 1, Qt.AlignRight)

            # Lay out the model details as per the descriptors
            (labPos, valPos) = (1, 0) if self.inverted else (0, 1)
            (labAlign, valAlign) = (Qt.AlignLeft, Qt.AlignRight) if self.inverted else (Qt.AlignRight, Qt.AlignLeft)
            (labAlign, valAlign) = (labAlign, valAlign) if self.displayMode == Details.DisplayMode.Central else (valAlign, labAlign)

            for i, descriptor in enumerate(self.descriptors):
                self.gridLayout.addWidget(self.labels[i], i, labPos, labAlign)
                self.gridLayout.addWidget(self.valueFormatter(descriptor)(self.model), i, valPos, valAlign)

            self.gridLayout.addWidget(self.toolBar, 0, 2, detailsCount, 1, Qt.AlignRight)
            self.gridLayout.setColumnStretch(0, 1)
            self.gridLayout.setColumnStretch(1, 1)
            self.gridLayout.setColumnStretch(2, 0)

        else:
            self.gridLayout.addWidget(QLabel('No data'), 0, 0, Qt.AlignCenter)

        self.adjustSize()
        rowHeight = self.gridLayout.geometry().height() / detailsCount if detailsCount > 0 else 0
        self.toolBar.setIconSize(QSize(rowHeight, rowHeight))