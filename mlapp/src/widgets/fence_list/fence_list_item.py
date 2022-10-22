# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QHBoxLayout, QLabel, QSizePolicy, QToolBar, QWidget

from ...models.state import State
from ...spatial.features.feature_status import FeatureStatus
from ...widgets.feature_status_label import FeatureStatusLabel


class FenceListItem(QWidget):
    layoutRefreshNeeded = pyqtSignal()

    # Editing signals
    plan = pyqtSignal()
    undoPlan = pyqtSignal()

    def __init__(self, fence, parent=None):
        super().__init__(parent)

        self.state = State()

        self.fence = fence

        self.titleLabel = QLabel()
        self.titleLabel.setText(
            f"Fence {self.fence.buildOrder}: ({self.fence.featureLength} km)")

        self.statusLabel = FeatureStatusLabel(None)

        self.toolBar = QToolBar()
        self.toolBar.setStyleSheet("""QToolBar { padding: 0; }
                                      QToolButton::indicator {
                                        height: 20;
                                        width: 20;
                                      }""")
        self.toolBar.setFixedHeight(30)

        self.undoPlanAction = QAction(QIcon(
            ':/plugins/mlapp/images/item-undo.png'), self.tr(u'Undo Plan Fence'), self)
        self.planAction = QAction(
            QIcon(':/plugins/mlapp/images/item-edit.png'), self.tr(u'Plan Fence'), self)
        self.zoomAction = QAction(QIcon(
            ':/plugins/mlapp/images/paddock-zoom.png'), self.tr(u'Zoom to Fence'), self)

        self.undoPlanAction.triggered.connect(lambda _: self.fence.undoPlanFence())
        self.toolBar.addAction(self.undoPlanAction)
        self.planAction.triggered.connect(lambda _: self.fence.planFence())
        self.toolBar.addAction(self.planAction)
        self.zoomAction.triggered.connect(self.selectFence)
        self.zoomAction.triggered.connect(self.fence.zoomToFeature)
        self.toolBar.addAction(self.zoomAction)

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

    def setStatus(self, status):
        self.statusLabel.setStatus(status)

    def refreshUi(self):
        """Refresh the UI based on the current state of the fence."""
        status = self.fence.status
        drafted = status == FeatureStatus.Drafted

        self.setStatus(status)

        self.titleLabel.setText(
            f"Fence {self.fence.buildOrder}: ({self.fence.featureLength} km)")

        # Hide or show toolbar items
        self.undoPlanAction.setVisible(not drafted)
        self.planAction.setVisible(drafted)

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def selectFence(self):
        """Select this Fence."""
        project = self.state.getProject()
        if project is not None:
            project.setSelectedFence(self.fence)

    def zoomToFence(self, title):
        """Select this Fence and zoom to it."""
        self.selectFence()
        self.fence.zoomToFeature()

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.

        hint = QSize(self.layout.sizeHint().width(),
                     self.layout.sizeHint().height())
        return hint
