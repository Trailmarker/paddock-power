# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QSizePolicy, QVBoxLayout, QWidget

from ...models.state import State
from ..edit_state_machine import EditAction, EditStateMachine, EditStatus
from ..collapse.collapse import Collapse


class FeatureCollapsibleListItem(QWidget, EditStateMachine):
    layoutRefreshNeeded = pyqtSignal()

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
            ':/plugins/mlapp/images/item-undo.png'), f"Cancel Editing {feature.displayName()}", self)
        self.saveAction = QAction(
            QIcon(':/plugins/mlapp/images/item-save.png'), f"Save Changes to {feature.displayName()}", self)
        self.editAction = QAction(
            QIcon(':/plugins/mlapp/images/item-edit.png'), (f"Edit a{feature.displayName()}"), self)
        self.zoomAction = QAction(QIcon(
            ':/plugins/mlapp/images/paddock-zoom.png'), self.tr(f"Zoom to {feature.displayName()}"), self)
        # self.selectAction = QAction(QIcon(
        #     ':/plugins/mlapp/images/paddock-zoom.png'), self.tr(f"Select {feature.displayName()}"), self)

        self.collapse.addToolBarAction(self.cancelEditAction, lambda: self.cancelEditItem())
        self.collapse.addToolBarAction(self.saveAction, lambda: self.saveItem())
        self.collapse.addToolBarAction(self.editAction, lambda: self.editItem())
        self.collapse.addToolBarAction(self.zoomAction, self.selectFeature)
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

        self.stateChanged.connect(self.refreshUi)

        self.refreshUi()

    @EditAction.edit.handler()
    def editItem(self):
        self.collapse.setExpanded(True)

    @EditAction.save.handler()
    def saveItem(self):
        self.featureEdit.savePaddock()
        pass

    @EditAction.cancelEdit.handler()
    def cancelEditItem(self):
        pass

    def refreshUi(self):
        self.collapse.setFeatureStatus(self.feature.status)

        # Set title to paddock name with some details
        self.setTitle(
            f"{self.feature.name} ({self.feature.featureArea} km², ?? AE)")

        permitted = self.allPermitted()

        # Hide or show forms
        editing = self.status == EditStatus.Editing
        self.featureDetails.setVisible(not editing)
        self.featureEdit.setVisible(editing)

        # Hide or show collapse toolbar items
        self.cancelEditAction.setVisible(EditAction.cancelEdit in permitted)
        self.saveAction.setVisible(EditAction.save in permitted)
        self.editAction.setVisible(EditAction.edit in permitted)

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def setTitle(self, title):
        self.collapse.setTitle(title)

    def selectFeature(self):
        """Select this paddock."""
        # self.collapse.setExpanded(True)
        milestone = self.state.getMilestone()
        if milestone is not None:
            milestone.setSelectedFeature(self.feature)

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.
        hint = QSize(self.collapse.sizeHint().width(),
                     self.collapse.sizeHint().height())
        return hint
