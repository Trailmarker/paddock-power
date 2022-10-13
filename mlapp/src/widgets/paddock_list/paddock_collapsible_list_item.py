# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QSize, QState, QStateMachine
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QSizePolicy, QVBoxLayout, QWidget

from qgis.core import QgsRectangle
from qgis.utils import iface

from ...models.paddock_power_state import PaddockPowerState
from ..collapse.collapse import Collapse
from ..paddock_details.paddock_details import PaddockDetails
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit
from ...utils import qgsDebug

class PaddockCollapsibleListItem(QWidget):
    layoutRefreshNeeded = pyqtSignal()

    # Editing signals
    edit = pyqtSignal()
    save = pyqtSignal()
    cancelEdit = pyqtSignal()

    def __init__(self, paddock, parent=None):
        super(QWidget, self).__init__(parent)

        self.state = PaddockPowerState()

        self.paddock = paddock
        self.paddockDetails = PaddockDetails(paddock)
        self.paddockDetailsEdit = PaddockDetailsEdit(paddock)

        # Swap between view and edit layouts in the Collapse widget content area
        self.collapseLayout = QVBoxLayout()
        self.collapseLayout.setSpacing(0)
        self.collapseLayout.setContentsMargins(0, 0, 0, 0)
        self.collapseLayout.addWidget(self.paddockDetails)
        self.collapseLayout.addWidget(self.paddockDetailsEdit)
        self.collapseLayout.addStretch()

        self.collapse = Collapse(self)
        self.collapse.setContentLayout(self.collapseLayout)

        self.cancelEditAction = QAction(QIcon(
            ':/plugins/mlapp/images/item-undo.png'), self.tr(u'Cancel Editing Paddock'), self)
        self.saveAction = QAction(
            QIcon(':/plugins/mlapp/images/item-save.png'), self.tr(u'Save Changes to Paddock'), self)
        self.editAction = QAction(
            QIcon(':/plugins/mlapp/images/item-edit.png'), self.tr(u'Edit Paddock'), self)
        self.zoomAction = QAction(QIcon(
            ':/plugins/mlapp/images/paddock-zoom.png'), self.tr(u'Zoom to Paddock'), self)

        # self.collapse.addToolBarAction(QAction(QIcon(':/plugins/mlapp/images/paddock.png'), self.tr(u'Select Paddock'), self), self.selectPaddock)
        self.collapse.addToolBarAction(
            self.cancelEditAction, self.cancelEdit.emit)
        self.collapse.addToolBarAction(self.saveAction, self.save.emit)
        self.collapse.addToolBarAction(self.editAction, self.edit.emit)
        self.collapse.addToolBarAction(self.zoomAction, self.zoomToPaddock)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.collapse)
        layout.addStretch()

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(layout)

        self.collapse.collapsed.connect(self.layoutRefreshNeeded.emit)
        self.collapse.expanded.connect(self.layoutRefreshNeeded.emit)

        # Set up state machine
        self.machine = QStateMachine()

        self.viewState = QState()
        self.editState = QState()

        self.viewState.addTransition(self.edit, self.editState)
        self.editState.addTransition(self.save, self.viewState)
        self.editState.addTransition(self.cancelEdit, self.viewState)

        self.save.connect(self.paddockDetailsEdit.savePaddock)

        self.machine.addState(self.viewState)
        self.machine.addState(self.editState)
        self.machine.setInitialState(self.viewState)

        self.viewState.entered.connect(self.refreshUi)
        self.editState.entered.connect(self.refreshUi)
        self.editState.entered.connect(self.collapse.setExpanded)
        self.machine.started.connect(self.refreshUi)
        self.machine.start()

        self.refreshUi()

    def refreshUi(self):
        editing = self.editState in self.machine.configuration()

        # Set title to paddock name with some details
        self.setTitle(f"{self.paddock.paddockName()} ({self.paddock.paddockArea()} km², ?? AE)")

        # Hide or show forms
        self.paddockDetails.setVisible(not editing)
        self.paddockDetailsEdit.setVisible(editing)

        # Hide or show collapse toolbar items
        self.cancelEditAction.setVisible(editing)
        self.saveAction.setVisible(editing)
        self.editAction.setVisible(not editing)

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def setTitle(self, title):
        self.collapse.setTitle(title)

    def selectPaddock(self):
        """Select this paddock."""
        # self.collapse.setExpanded(True)
        milestone = self.state.getMilestone()
        if milestone is not None:
            milestone.setSelectedPaddock(self.paddock)

    def zoomToPaddock(self, title):
        """Select this paddock and zoom to it."""
        self.selectPaddock()
        paddockExtent = QgsRectangle(self.paddock.geometry().boundingBox())
        paddockExtent.scale(1.5)  # Expand by 50%
        iface.mapCanvas().setExtent(paddockExtent)
        iface.mapCanvas().refresh()

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.
        hint = QSize(self.collapse.sizeHint().width(),
                     self.collapse.sizeHint().height())
        return hint
