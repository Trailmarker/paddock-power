# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from ..collapse.collapse import Collapse
from ..edit_state_machine import EditAction, EditStateMachine, EditStatus
from ..feature_status_label.feature_status_label import FeatureStatusLabel
from ..state_machine_tool_bar.state_machine_tool_bar import StateMachineToolBar


class PersistedFeatureCollapsibleListItem(QWidget, EditStateMachine):
    layoutRefreshNeeded = pyqtSignal()

    def __init__(self, feature, DetailsWidget, EditWidget, parent=None):
        super().__init__(parent)

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

        self.statusLabel = FeatureStatusLabel(None)

        self.toolBar = StateMachineToolBar(self)

        self.toolBar.addStateAction(EditAction.edit, ':/plugins/mlapp/images/edit-item.png', lambda *_: self.editItem())
        self.toolBar.addStateAction(
            EditAction.cancelEdit,
            ':/plugins/mlapp/images/cancel-edit-item.png',
            lambda *_: self.cancelEditItem())
        self.toolBar.addStateAction(EditAction.save, ':/plugins/mlapp/images/save-item.png', lambda *_: self.saveItem())
        self.toolBar.addGenericAction(
            ':/plugins/mlapp/images/zoom-item.png',
            f"Zoom to {self.feature.displayName()}",
            lambda *_: self.selectFeature())

        self.collapse = Collapse(self)
        self.collapse.setContentLayout(self.collapseLayout)
        self.collapse.addHeaderWidget(self.statusLabel)
        self.collapse.addHeaderWidget(self.toolBar)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.collapse)
        layout.addStretch()

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(layout)

        self.collapse.collapsed.connect(self.layoutRefreshNeeded.emit)
        self.collapse.expanded.connect(self.layoutRefreshNeeded.emit)

        self.feature.stateChanged.connect(self.refreshUi)
        self.stateChanged.connect(self.refreshUi)

        self.refreshUi()

    def displayName(self):
        return self.feature.displayName()

    @EditAction.edit.handler()
    def editItem(self):
        self.collapse.setExpanded(True)

    @EditAction.save.handler()
    def saveItem(self):
        self.featureEdit.saveFeature()
        pass

    @EditAction.cancelEdit.handler()
    def cancelEditItem(self):
        pass

    def refreshUi(self):
        # Set title to paddock name with some details
        self.collapse.setTitle(
            f"{self.feature.name} ({self.feature.featureArea} km², {self.feature.estimatedCapacity:g} AE)")

        self.statusLabel.status = self.feature.status

        # Hide or show forms
        editing = self.status == EditStatus.Editing
        self.featureDetails.setVisible(not editing)
        self.featureEdit.setVisible(editing)

        self.toolBar.refreshUi()

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def selectFeature(self):
        """Select this Persisted Feature (and zoom to it)."""
        self.feature.selectFeature()

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.
        hint = QSize(self.collapse.sizeHint().width(),
                     self.collapse.sizeHint().height())
        return hint
