# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QSize, QState, QStateMachine
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QHBoxLayout, QLabel, QSizePolicy, QToolBar, QWidget

from qgis.core import QgsRectangle
from qgis.utils import iface

from ...models.paddock_power_state import PaddockPowerState
from ...spatial.feature.feature_status import FeatureStatus
from ...spatial.feature.fence import Fence
from ...utils import qgsDebug


class FenceListItem(QWidget):
    layoutRefreshNeeded = pyqtSignal()

    # Editing signals
    plan = pyqtSignal()
    undoPlan = pyqtSignal()

    def __init__(self, fence, parent=None):
        super().__init__(parent)

        self.state = PaddockPowerState()

        self.fence = fence

        self.titleLabel = QLabel()
        self.titleLabel.setText(
            f"Fence {self.fence.fenceBuildOrder()}: ({self.fence.featureLength()} km)")

        self.toolBar = QToolBar()
        self.toolBar.setStyleSheet("""QToolBar { padding: 0; }
                                      QToolButton::indicator {
                                        height: 20;
                                        width: 20;
                                      }""")
        self.toolBar.setFixedHeight(30)
        self.toolBar.setSizePolicy(QSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.undoPlanAction = QAction(QIcon(
            ':/plugins/mlapp/images/item-undo.png'), self.tr(u'Undo Plan Fence'), self)
        self.planAction = QAction(
            QIcon(':/plugins/mlapp/images/item-edit.png'), self.tr(u'Plan Fence'), self)
        self.zoomAction = QAction(QIcon(
            ':/plugins/mlapp/images/paddock-zoom.png'), self.tr(u'Zoom to Fence'), self)

        self.undoPlanAction.triggered.connect(self.undoPlan.emit)
        self.toolBar.addAction(self.undoPlanAction)
        self.planAction.triggered.connect(self.plan.emit)
        self.toolBar.addAction(self.planAction)
        self.zoomAction.triggered.connect(self.zoomToFence)
        self.toolBar.addAction(self.zoomAction)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(3, 0, 3, 3)
        self.layout.addWidget(self.titleLabel)
        self.layout.addStretch()
        self.layout.addWidget(self.toolBar)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(self.layout)

        # Set up state machine
        self.machine = QStateMachine()

        self.draftedState = QState()
        self.plannedState = QState()

        self.draftedState.addTransition(self.plan, self.plannedState)
        self.plannedState.addTransition(self.undoPlan, self.draftedState)

        self.machine.addState(self.draftedState)
        self.machine.addState(self.plannedState)

        self.machine.setInitialState(self.plannedState
                                     if fence.status() == FeatureStatus.Planned
                                     else self.draftedState)

        self.plan.connect(self.planFence)
        self.undoPlan.connect(self.undoPlanFence)

        self.draftedState.entered.connect(self.refreshUi)
        self.plannedState.entered.connect(self.refreshUi)

        self.machine.start()

        self.refreshUi()

    def refreshUi(self):
        drafted = self.draftedState in self.machine.configuration()

        self.titleLabel.setText(
            f"Fence {self.fence.fenceBuildOrder()}: ({self.fence.featureLength()} km)")
        if drafted:
            self.titleLabel.setStyleSheet("background-color: rgb(242,212,215)")

        # Hide or show toolbar items
        self.undoPlanAction.setVisible(not drafted)
        self.planAction.setVisible(drafted)

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def planFence(self):
        milestone = self.state.getMilestone()
        qgsDebug(
            f"FenceListItem.planFence: self.fence.__class__.__name__ = {self.fence.__class__.__name__}")
        qgsDebug(
            f"FenceListItem.planFence: isinstance(self.fence, Fence) = {str(isinstance(self.fence, Fence))}")
        if milestone is not None:
            milestone.planFence(self.fence)

    def undoPlanFence(self):
        milestone = self.state.getMilestone()
        qgsDebug(
            f"FenceListItem.undoPlanFence: self.fence.__class__.__name__ = {self.fence.__class__.__name__}")
        qgsDebug(
            f"FenceListItem.undoPlanFence: isinstance(self.fence, Fence) = {str(isinstance(self.fence, Fence))}")
        if milestone is not None:
            milestone.undoPlanFence(self.fence)

    def selectFence(self):
        """Select this paddock."""
        # self.collapse.setExpanded(True)
        milestone = self.state.getMilestone()
        if milestone is not None:
            milestone.setSelectedFence(self.fence)

    def zoomToFence(self, title):
        """Select this paddock and zoom to it."""
        self.selectFence()
        fenceExtent = QgsRectangle(self.fence.geometry().boundingBox())
        fenceExtent.scale(1.5)  # Expand by 50%
        iface.mapCanvas().setExtent(fenceExtent)
        iface.mapCanvas().refresh()

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.
        hint = QSize(self.layout.sizeHint().width(),
                     self.layout.sizeHint().height())
        return hint
