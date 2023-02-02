# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from ...models import QtAbstractMeta, toStateMachine
from ...layers.features import Edits, FeatureAction
from ...utils import PLUGIN_FOLDER, qgsDebug
from ..collapse.collapse import Collapse
from ..edit_state_machine import EditAction, EditStateMachine, EditStatus
from ..feature_status_label.feature_status_label import FeatureStatusLabel
from ..state_machine_tool_bar.state_machine_tool_bar import StateMachineToolBar
from .status_feature_tool_bar import StatusFeatureToolBar


class FeatureListItem(QWidget, EditStateMachine, metaclass=QtAbstractMeta):
    _stateChanged = pyqtSignal()
    layoutRefreshNeeded = pyqtSignal()

    def __init__(self, feature, detailsWidgetFactory=None, editWidgetFactory=None, parent=None):
        QWidget.__init__(self, parent)
        EditStateMachine.__init__(self)

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
            self.statusToolBar = StatusFeatureToolBar(self.feature)

            self.statusToolBar.addStateAction(
                FeatureAction.undoPlan,
                f':/plugins/{PLUGIN_FOLDER}/images/undo-plan-feature.png',
                lambda _: self.feature.undoPlanFeature())
            self.statusToolBar.addStateAction(
                FeatureAction.plan,
                f':/plugins/{PLUGIN_FOLDER}/images/plan-feature.png',
                lambda _: self.feature.planFeature())
            self.statusToolBar.addStateAction(
                FeatureAction.undoBuild,
                f':/plugins/{PLUGIN_FOLDER}/images/undo-build-feature.png',
                lambda _: self.feature.undoBuildFeature())
            self.statusToolBar.addStateAction(
                FeatureAction.build,
                f':/plugins/{PLUGIN_FOLDER}/images/build-feature.png',
                lambda _: self.feature.buildFeature())
            self.statusToolBar.addStateAction(
                FeatureAction.trash,
                f':/plugins/{PLUGIN_FOLDER}/images/trash-feature.png',
                lambda _: self.feature.trashFeature())

            self.collapse.addHeaderWidget(self.statusLabel)
            self.collapse.addHeaderWidget(self.statusToolBar)

        # Create toolbar for Feature editing (if applicable)
        self.editToolBar = StateMachineToolBar(self)

        self.editToolBar.addStateAction(
            EditAction.edit,
            f':/plugins/{PLUGIN_FOLDER}/images/edit-item.png',
            lambda *_: self.editItem())
        self.editToolBar.addStateAction(
            EditAction.cancelEdit,
            f':/plugins/{PLUGIN_FOLDER}/images/cancel-edit-item.png',
            lambda *_: self.cancelEditItem())

        self.editToolBar.addStateAction(
            EditAction.save,
            f':/plugins/{PLUGIN_FOLDER}/images/save-item.png',
            lambda *_: self.saveItem())
    
        self.editToolBar.addGenericAction(
            f':/plugins/{PLUGIN_FOLDER}/images/zoom-item.png',
            f"Zoom to {self.feature.displayName()}",
            lambda *_: self.selectFeature())

        if not self.isEditable:
            self.editToolBar.hideStateActions()

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
            toStateMachine(self.feature).stateChanged.connect(self.refreshUi)
        self.refreshUi()

    def setSelected(self, selected):
        if selected:
            self.collapse.toggleButton.setStyleSheet("background-color: yellow")
        else:
            self.collapse.toggleButton.setStyleSheet("background-color: white")
            

    @property
    def stateChanged(self):
        return self._stateChanged

    def emitStateChanged(self):
        self._stateChanged.emit()

    @property
    def hasDetails(self):
        return self.featureDetails is not None

    @property
    def hasStatus(self):
        return self.feature and self.feature.hasStatus

    @property
    def hasTimeFrame(self):
        return self.feature and self.feature.hasTimeframe

    @property
    def isEditable(self):
        return self.featureEdit is not None

    def hideStatusControls(self):
        """Hide the status controls (e.g. for a specific list widget)."""
        self.statusToolBar.hideStateActions()
        self.refreshUi()

    def hideEditControls(self):
        """Hide the edit controls (e.g. for a specific list widget)."""
        self.editToolBar.hideStateActions()
        self.refreshUi()

    def displayName(self):
        return self.feature.displayName()

    @EditAction.edit.handler()
    def editItem(self):
        self.collapse.setExpanded(True)

    @Edits.persistFeatures
    @EditAction.save.handler()
    def saveItem(self):
        # saveFeature returns an Edits …
        return self.featureEdit.saveFeature()

    @EditAction.cancelEdit.handler()
    def cancelEditItem(self):
        pass

    def selectFeature(self):
        """Select this Persisted Feature (and zoom to it)."""
        self.feature.selectFeature()

    def refreshUi(self):
        """Refresh the UI based on the current state of the fence."""

        # Set title to Feature title
        self.collapse.setTitle(self.feature.TITLE)

        if self.hasStatus:
            self.statusLabel.status = self.feature.STATUS
            self.statusToolBar.refreshUi()

        if self.isEditable:
            # Hide or show forms
            editing = self.status == EditStatus.Editing
            self.featureDetails.setVisible(not editing)
            self.featureEdit.setVisible(editing)

            # Hide status workflow functions when in edit mode
            if self.hasStatus:
                self.statusToolBar.setVisible(not editing)

        self.editToolBar.refreshUi()

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse widget controls the width.
        hint = QSize(self.collapse.sizeHint().width(),
                     self.collapse.sizeHint().height())
        return hint
