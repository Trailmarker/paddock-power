# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from ...spatial.features.feature_action import FeatureAction
from ...spatial.features.status_feature import StatusFeature
from ..collapse.collapse import Collapse
from ..edit_state_machine import EditAction, EditStateMachine, EditStatus
from ..feature_status_label.feature_status_label import FeatureStatusLabel
from ..state_tool_bar.state_tool_bar import StateToolBar
from .feature_tool_bar import FeatureToolBar


class FeatureListItemNew(QWidget, EditStateMachine):
    layoutRefreshNeeded = pyqtSignal()

    def __init__(self, feature, detailsWidgetFactory, editWidgetFactory=None, parent=None):
        super().__init__(parent)

        self.feature = feature

        # Swap between view and edit layouts in the Collapse widget content area
        self.collapseLayout = QVBoxLayout()
        self.collapseLayout.setSpacing(0)
        self.collapseLayout.setContentsMargins(0, 0, 0, 0)

        # We do things differently based on whether we have details and editing
        if detailsWidgetFactory:
            self.featureDetails = detailsWidgetFactory(feature)
            self.collapseLayout.addWidget(self.featureDetails)

            if editWidgetFactory:
                self.featureEdit = editWidgetFactory(feature)
                self.collapseLayout.addWidget(self.featureEdit)
            else:
                self.featureEdit = None
        else:
            self.featureDetails = None
            self.featureEdit = None

        self.collapseLayout.addStretch()
        self.collapse = Collapse(self)
        self.collapse.setContentLayout(self.collapseLayout)

        # Create toolbar for Feature workflow
        if self.hasStatus:
            self.statusLabel = FeatureStatusLabel(None)

            self.statusToolBar = FeatureToolBar(self.feature)

            self.statusToolBar.addStateAction(
                FeatureAction.undoPlan,
                ':/plugins/mlapp/images/undo-plan-feature.png',
                lambda _: self.feature.undoPlanFeature())
            self.statusToolBar.addStateAction(
                FeatureAction.plan,
                ':/plugins/mlapp/images/plan-feature.png',
                lambda _: self.feature.planFeature())
            self.statusToolBar.addStateAction(
                FeatureAction.undoBuild,
                ':/plugins/mlapp/images/undo-build-feature.png',
                lambda _: self.feature.undoBuildFeature())
            self.statusToolBar.addStateAction(
                FeatureAction.build,
                ':/plugins/mlapp/images/build-feature.png',
                lambda _: self.feature.buildFeature())
            self.statusToolBar.addStateAction(
                FeatureAction.trash,
                ':/plugins/mlapp/images/trash-feature.png',
                lambda _: self.feature.trashFeature())

            self.collapse.addHeaderWidget(self.statusLabel)
            self.collapse.addHeaderWidget(self.statusToolBar)

        # Create toolbar for Feature editing (if applicable)
        self.editToolBar = StateToolBar(self)

        if self.isEditable:

            self.editToolBar.addStateAction(
                EditAction.edit,
                ':/plugins/mlapp/images/edit-item.png',
                lambda *_: self.editItem())
            self.editToolBar.addStateAction(
                EditAction.cancelEdit,
                ':/plugins/mlapp/images/cancel-edit-item.png',
                lambda *_: self.cancelEditItem())
            self.editToolBar.addStateAction(
                EditAction.save,
                ':/plugins/mlapp/images/save-item.png',
                lambda *_: self.saveItem())

        self.editToolBar.addGenericAction(
            ':/plugins/mlapp/images/zoom-item.png',
            f"Zoom to {self.feature.displayName()}",
            lambda *_: self.selectFeature())

        self.collapse.addHeaderWidget(self.editToolBar)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.collapse)
        layout.addStretch()

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(layout)

        if not self.hasDetails:
            self.collapse.setCollapseEnabled(False)
        else:
            self.collapse.collapsed.connect(self.layoutRefreshNeeded.emit)
            self.collapse.expanded.connect(self.layoutRefreshNeeded.emit)

        # Respond to changes in editing status
        self.stateChanged.connect(self.refreshUi)

        if self.hasStatus:
            self.feature.stateChanged.connect(self.refreshUi)

        self.refreshUi()

    @property
    def hasDetails(self):
        return self._featureDetails is not None

    @property
    def hasStatus(self):
        return isinstance(self.feature, StatusFeature)

    @property
    def isEditable(self):
        return self._featureEdit is not None

    @property
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

    def selectFeature(self):
        """Select this Persisted Feature (and zoom to it)."""
        self.feature.selectFeature()

    def refreshUi(self):
        """Refresh the UI based on the current state of the fence."""

        # Set title to Feature title
        self.collapse.setTitle(self.feature.title)
        # f"{self.feature.name} ({self.feature.featureArea} km², {self.feature.estimatedCapacity:g} AE)")

        if self.hasStatus:
            self.statusLabel.status = self.feature.status

        if self.isEditable:

            # Hide or show forms
            editing = self.status == EditStatus.Editing
            self.featureDetails.setVisible(not editing)
            self.featureEdit.setVisible(editing)

            self.editToolbar.refreshUi()

        self.statusToolBar.refreshUi()

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.

        hint = QSize(self.layout.sizeHint().width(),
                     self.layout.sizeHint().height())
        return hint
