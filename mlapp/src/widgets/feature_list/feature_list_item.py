# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

from ...spatial.features.feature_action import FeatureAction
from ..feature_status_label.feature_status_label import FeatureStatusLabel
from .feature_tool_bar import FeatureToolBar


class FeatureListItem(QWidget):
    layoutRefreshNeeded = pyqtSignal()

    def __init__(self, feature, parent=None):
        super().__init__(parent)

        self.feature = feature

        self.titleLabel = QLabel()
        self.titleLabel.setText(self.feature.title)

        self.statusLabel = FeatureStatusLabel(None)

        self.toolBar = FeatureToolBar(self.feature)

        self.toolBar.addStateAction(
            FeatureAction.undoPlan,
            ':/plugins/mlapp/images/undo-plan-feature.png',
            lambda _: self.feature.undoPlanFeature())
        self.toolBar.addStateAction(
            FeatureAction.plan,
            ':/plugins/mlapp/images/plan-feature.png',
            lambda _: self.feature.planFeature())
        self.toolBar.addStateAction(
            FeatureAction.trash,
            ':/plugins/mlapp/images/trash-feature.png',
            lambda _: self.feature.trashFeature())
        self.toolBar.addSelectAction()

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
        self.statusLabel.status = self.feature.status
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
