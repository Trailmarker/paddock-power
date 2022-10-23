# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

from ...models.state import State
from ...spatial.features.feature_action import FeatureAction
from ..feature_status_label import FeatureStatusLabel
from .feature_tool_bar import FeatureToolBar


class FeatureListItem(QWidget):
    layoutRefreshNeeded = pyqtSignal()

    # Editing signals
    plan = pyqtSignal()
    undoPlan = pyqtSignal()

    def __init__(self, feature, parent=None):
        super().__init__(parent)

        self.state = State()

        self.feature = feature

        self.titleLabel = QLabel()
        self.titleLabel.setText(self.feature.title)

        self.statusLabel = FeatureStatusLabel(None)

        self.toolBar = FeatureToolBar(self.feature)

        self.toolBar.addFeatureAction(
            FeatureAction.undoPlan,
            ':/plugins/mlapp/images/item-undo.png',
            lambda _: self.feature.undoPlanFence())
        self.toolBar.addFeatureAction(
            FeatureAction.plan,
            ':/plugins/mlapp/images/item-edit.png',
            lambda _: self.feature.planFence())
        self.toolBar.addFeatureAction(
            FeatureAction.plan,
            ':/plugins/mlapp/images/delete-project.png',
            lambda _: self.feature.trashFeature())
        self.toolBar.addZoomAction()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(3, 0, 3, 3)
        self.layout.addWidget(self.titleLabel)
        self.layout.addStretch()
        self.layout.addWidget(self.statusLabel)
        self.layout.addWidget(self.toolBar)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(self.layout)

        self.refreshUi()

    def refreshUi(self):
        """Refresh the UI based on the current state of the fence."""
        self.statusLabel.setStatus(self.feature.status)
        self.titleLabel.setText(self.feature.title)
        self.toolBar.refreshUi()

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.

        hint = QSize(self.layout.sizeHint().width(),
                     self.layout.sizeHint().height())
        return hint
