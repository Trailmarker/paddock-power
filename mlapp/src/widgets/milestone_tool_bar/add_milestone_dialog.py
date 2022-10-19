# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDialog

from ...models.glitch import Glitch
from ...models.project import Project

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'add_milestone_dialog_base.ui')))


class AddMilestoneDialog(QDialog, FORM_CLASS):
    def __init__(self, project, parent=None):
        """Constructor."""
        if project is None:
            raise Glitch("AddMilestoneDialog: project is empty")
        if not isinstance(project, Project):
            raise Glitch(
                "AddMilestoneDialog: project is not a Project")

        super().__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(":/plugins/mlapp/images/new-milestone.png"))

        if project.milestone is not None:
            self.setWindowTitle(
                f"Add Milestone from '{project.milestone.milestoneName}'")

        self.project = project

        self.milestoneNameLineEdit.textChanged.connect(self.clearError)

    def reject(self):
        """Reject the dialog."""
        super(AddMilestoneDialog, self).reject()

    def accept(self):
        """Accept the dialog."""
        newMilestoneName = self.milestoneNameLineEdit.text()

        if not newMilestoneName:
            self.setError("Your Milestone name is empty.")
            return

        if not newMilestoneName.isalnum():
            self.setError("Use letters, numbers and spaces only.")
            return

        if newMilestoneName in self.project.milestones:
            self.setError("Your Milestone name is not unique.")
            return

        super(AddMilestoneDialog, self).accept()

    def clearError(self):
        """Clear the error message."""
        self.errorLabel.setText("")

    def setError(self, errorMessage):
        """Set the error message."""
        self.errorLabel.setText(errorMessage)