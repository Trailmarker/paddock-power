# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDockWidget

from .add_milestone_dialog import AddMilestoneDialog
from .paddock_table_model import PaddockTableModel
from ..models.state import detectProject, getState, getProject
from ..utils import guiConfirm, qgsDebug

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_view_dock_widget_base.ui')))


class PaddockViewDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()
    renderNeeded = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(QDockWidget, self).__init__(parent)

        self.setupUi(self)

        self.addMilestoneButton.setIcon(
            QIcon(":/plugins/mlapp/images/new-milestone.png"))
        self.deleteMilestoneButton.setIcon(
            QIcon(":/plugins/mlapp/images/delete-milestone.png"))

        self.addMilestoneButton.clicked.connect(self.addMilestone)
        self.deleteMilestoneButton.clicked.connect(self.deleteMilestone)

        detectProject()

        getState().projectChanged.connect(self.setupConnections)
        getState().projectChanged.connect(self.render)
        self.milestoneComboBox.currentIndexChanged.connect(
            self.milestoneComboBoxChanged)

        self.renderNeeded.connect(self.render)

        self.render()

    def setupConnections(self):
        """Reconnect things as necessary."""
        project = getProject()
        if project is not None:
            project.currentMilestoneChanged.connect(self.render)

    def showEvent(self, event):
        qgsDebug("Show Event")
        detectProject()

        # self.render()

    def render(self):
        """Show the Paddock View."""

        # qgsDebug("Rendering")

        project = getProject()

        # qgsDebug(f"Project: {str(project)}")
        # qgsDebug(f"Current Milestone: {str(project.currentMilestone)}")
        # qgsDebug(f"Milestones: {str([m.milestoneName for m in project.milestones.values()])}")

        self.milestoneComboBox.blockSignals(True)

        if project is None:
            self.milestoneComboBox.clear()
            self.milestoneComboBox.setEnabled(False)
            self.addMilestoneButton.setEnabled(False)
            self.deleteMilestoneButton.setEnabled(False)

            self.tableView.setModel(PaddockTableModel(None))
            return

        # project.load(True)

        self.milestoneComboBox.clear()
        milestoneNames = [
            milestoneName for milestoneName in project.milestones.keys()]
        milestoneNames.sort()
        milestoneNames.insert(0, '')
        self.milestoneComboBox.addItems(milestoneNames)

        self.addMilestoneButton.setEnabled(True)
        self.addMilestoneButton.toolTip = "Add a new Milestone …"

        if project.currentMilestone is not None:
            self.milestoneComboBox.setCurrentText(
                project.currentMilestone.milestoneName)
            tableModel = PaddockTableModel(
                project.currentMilestone.paddockLayer)
            self.tableView.setModel(tableModel)

            self.addMilestoneButton.toolTip = "Add a new Milestone based on the current Milestone …"
            self.deleteMilestoneButton.setEnabled(True)

        self.milestoneComboBox.blockSignals(False)

    def milestoneComboBoxChanged(self, index):
        """Switch the active milestone."""
        milestoneName = self.milestoneComboBox.itemText(index)
        qgsDebug(f"milestoneComboBoxChanged: {milestoneName}")
        if milestoneName:
            project = getProject()
            if project is not None:
                qgsDebug(f"Setting current milestone to {milestoneName}")
                project.setMilestone(milestoneName)
                self.renderNeeded.emit()

    def addMilestone(self):
        """Add a new milestone."""
        project = getProject()

        if project is None:
            return

        dialog = AddMilestoneDialog(project)
        if dialog.exec_():
            newMilestoneName = dialog.milestoneNameLineEdit.text()
            if project.currentMilestone is not None:
                existingMilestoneName = project.currentMilestone.milestoneName
                project.addMilestoneFromExisting(
                    milestoneName=newMilestoneName, existingMilestoneName=existingMilestoneName)
            else:
                project.addMilestone(newMilestoneName)

        self.renderNeeded.emit()

    def deleteMilestone(self):
        """Delete the active milestone."""
        project = getProject()

        if project is None:
            return

        if project.currentMilestone is not None:
            confirmed = guiConfirm(
                f"Are you sure you want to delete the Milestone '{project.currentMilestone.milestoneName}'?", "Delete current Milestone")
            if confirmed:
                project.deleteMilestone(project.currentMilestone.milestoneName)
                self.renderNeeded.emit()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
