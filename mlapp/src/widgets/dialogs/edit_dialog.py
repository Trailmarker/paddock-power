# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from .dialog import Dialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'edit_dialog_base.ui')))


class EditDialog(Dialog, FORM_CLASS):
    """A dialog for editing a feature."""

    def __init__(self, feature, editWidgetFactory, parent=None):
        """Constructor."""
        Dialog.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self.feature = feature

        self.editWidget = editWidgetFactory(self.feature, self)
        self.editLayout.addWidget(self.editWidget)

        self.setWindowTitle(f"{self.feature.TITLE}")
        self.cancelButton.clicked.connect(self.reject)
        self.saveButton.clicked.connect(self.accept)

    @property
    def dialogRole(self):
        return "Edit"

    def showEvent(self, event):
        self.adjustSize()
        super().showEvent(event)

    def accept(self):
        self.workspace.saveEditsAndDerive(self.editWidget.saveFeature)
        super().accept()

    def reject(self):
        self.feature = None
        super().reject()
