# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QWidget

from ...models.paddock_power_state import PaddockPowerState, connectPaddockPowerStateListener
from ...utils import guiConfirm
from .add_milestone_dialog import AddMilestoneDialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'milestone_tool_bar_base.ui')))


class MilestoneToolBar(QWidget, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(MilestoneToolBar, self).__init__(parent)

        self.setupUi(self)

        self.state = PaddockPowerState()
        connectPaddockPowerStateListener(self.state, self)

        self.addMilestoneButton.setIcon(
            QIcon(":/plugins/mlapp/images/new-milestone.png"))
        self.deleteMilestoneButton.setIcon(
            QIcon(":/plugins/mlapp/images/delete-milestone.png"))

        self.addMilestoneButton.clicked.connect(self.addMilestone)
        self.deleteMilestoneButton.clicked.connect(self.deleteMilestone)

        self.milestoneComboBox.currentIndexChanged.connect(
            self.milestoneComboBoxChanged)

        self.refreshUi()

    @pyqtSlot()
    def onProjectChanged(self, project):
        """Handle a change in the current Paddock Power project."""
        self.refreshUi()

    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        """Handle a change in the current Paddock Power milestone."""
        self.refreshUi()

    @pyqtSlot()
    def onMilestonesUpdated(self, milestones):
        """Handle a change to the current collection of Paddock Power milestones."""
        self.refreshUi()

    def refreshUi(self):
        """Show the Paddock View."""

        project = self.state.getProject()

        self.milestoneComboBox.blockSignals(True)

        if project is None:
            self.milestoneComboBox.clear()
            self.milestoneComboBox.setEnabled(False)
            self.addMilestoneButton.setEnabled(False)
            self.deleteMilestoneButton.setEnabled(False)
            return

        self.milestoneComboBox.clear()
        milestoneNames = [
            milestoneName for milestoneName in project.milestones.keys()]
        milestoneNames.sort()
        milestoneNames.insert(0, '')
        self.milestoneComboBox.addItems(milestoneNames)

        self.addMilestoneButton.setEnabled(True)
        self.addMilestoneButton.toolTip = "Add a new Milestone …"

        if project.milestone is not None:
            self.milestoneComboBox.setCurrentText(
                project.milestone.milestoneName)
            self.addMilestoneButton.toolTip = "Add a new Milestone based on the current Milestone …"
            self.deleteMilestoneButton.setEnabled(True)

        self.milestoneComboBox.blockSignals(False)

    def milestoneComboBoxChanged(self, index):
        """Switch the active milestone."""
        milestoneName = self.milestoneComboBox.itemText(index)
        if milestoneName:
            project = self.state.getProject()
            if project is not None:
                project.setMilestone(milestoneName)

    def addMilestone(self):
        """Add a new milestone."""
        project = self.state.getProject()

        if project is None:
            return

        dialog = AddMilestoneDialog(project)
        if dialog.exec_():
            newMilestoneName = dialog.milestoneNameLineEdit.text()
            if project.milestone is not None:
                existingMilestoneName = project.milestone.milestoneName
                project.addMilestoneFromExisting(
                    milestoneName=newMilestoneName, existingMilestoneName=existingMilestoneName)
            else:
                project.addMilestone(newMilestoneName)

    def deleteMilestone(self):
        """Delete the active milestone."""
        project = self.state.getProject()

        if project is None:
            return

        if project.milestone is not None:
            confirmed = guiConfirm(
                f"Are you sure you want to delete the Milestone '{project.milestone.milestoneName}'?", "Delete current Milestone")
            if confirmed:
                project.deleteMilestone(project.milestone.milestoneName)
