# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from ...utils import PLUGIN_FOLDER
from ..collapse.collapse import Collapse
from ..edit_state_machine import EditAction, EditStateMachine, EditStatus
from ..state_machine_tool_bar.state_machine_tool_bar import StateMachineToolBar


class PaddockLandTypeListItem(QWidget, EditStateMachine):
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

        self.toolBar = StateMachineToolBar(self)

        self.toolBar.addStateAction(
            EditAction.edit,
            f':/plugins/{PLUGIN_FOLDER}/images/edit-item.png',
            lambda *_: self.editItem())
        self.toolBar.addStateAction(
            EditAction.cancelEdit,
            f':/plugins/{PLUGIN_FOLDER}/images/cancel-edit-item.png',
            lambda *_: self.cancelEditItem())
        self.toolBar.addStateAction(
            EditAction.save,
            f':/plugins/{PLUGIN_FOLDER}/images/save-item.png',
            lambda *_: self.saveItem())
        self.toolBar.addGenericAction(
            f':/plugins/{PLUGIN_FOLDER}/images/zoom-item.png',
            f"Zoom to {self.feature.displayName()}",
            lambda *_: self.selectFeature())

        self.collapse = Collapse(self)
        self.collapse.setContentLayout(self.collapseLayout)
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

        self.statusChanged = self.refreshUi
        self.feature.featureUpserted = self.refreshUi

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
            f"{self.feature.name} ({self.feature.FEATURE_AREA} km², {self.feature.estimatedCapacity:g} AE)")

        # Hide or show forms
        editing = self.status == EditStatus.Editing
        self.featureDetails.setVisible(not editing)
        self.featureEdit.setVisible(editing)

        self.toolBar.refreshUi()

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def selectFeature(self):
        """Select this Paddock Land Type and zoom to it."""
        self.feature.selectFeature()

    def sizeHint(self):
        """Return the size of the widget."""
        # The embedded Collapse item controls the width.
        hint = QSize(self.collapse.sizeHint().width(),
                     self.collapse.sizeHint().height())
        return hint
