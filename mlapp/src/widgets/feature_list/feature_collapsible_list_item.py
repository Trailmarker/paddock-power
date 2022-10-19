# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QSize, QState, QStateMachine
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QSizePolicy, QVBoxLayout, QWidget

from ...models.state import State
from ..edit_state_machine import EditStateMachine
from ..collapse.collapse import Collapse


class FeatureCollapsibleListItem(QWidget, EditStateMachine):
    layoutRefreshNeeded = pyqtSignal()

    # Editing signals
    edit = pyqtSignal()
    save = pyqtSignal()
    cancelEdit = pyqtSignal()

    def __init__(self, feature, DetailsWidget, EditWidget, parent=None):
        super().__init__(parent)

        self.state = State()

        self.feature = feature
        self.featureDetails = DetailsWidget(feature)
        self.featureEdit = EditWidget(feature)

        # Swap between view and edit layouts in the Collapse widget content area
        self.collapseLayout = QVBoxLayout()
        self.collapseLayout.setSpacing(0)
        self.collapseLayout.setContentsMargins(0, 0, 0, 0)
        self.collapseLayout.addWidget(self.featureDetails)
        self.collapseLayout.addWidget(self.featureEdit)
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
        self.collapse.addToolBarAction(self.zoomAction, self.selectPaddock)
        self.collapse.addToolBarAction(self.zoomAction, self.feature.zoomToFeature)

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

        self.save.connect(self.featureEdit.savePaddock)

        self.machine.addState(self.viewState)
        self.machine.addState(self.editState)
        self.machine.setInitialState(self.viewState)

        self.viewState.entered.connect(self.refreshUi)
        self.editState.entered.connect(self.refreshUi)
        self.editState.entered.connect(self.collapse.setExpanded)

        self.machine.start()

        self.refreshUi()

    def refreshUi(self):
        editing = self.editState in self.machine.configuration()

        self.setStatus(self.feature.status)

        # Set title to paddock name with some details
        self.setTitle(
            f"{self.feature.name} ({self.feature.featureArea} km², ?? AE)")

        # Hide or show forms
        self.featureDetails.setVisible(not editing)
        self.featureEdit.setVisible(editing)

        # Hide or show collapse toolbar items
        self.cancelEditAction.setVisible(editing)
        self.saveAction.setVisible(editing)
        self.editAction.setVisible(not editing)

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def setStatus(self, status):
        self.collapse.setStatus(status)

    def setTitle(self, title):
        self.collapse.setTitle(title)

    def selectPaddock(self):
        """Select this paddock."""
        # self.collapse.setExpanded(True)
        milestone = self.state.getMilestone()
        if milestone is not None:
            milestone.setSelectedPaddock(self.feature)

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.
        hint = QSize(self.collapse.sizeHint().width(),
                     self.collapse.sizeHint().height())
        return hint
