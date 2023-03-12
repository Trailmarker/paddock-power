# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

from ...models import WorkspaceMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'edit_dialog_base.ui')))


class EditDialog(QDialog, FORM_CLASS, WorkspaceMixin):
    """A dialog for editing a feature."""

    def __init__(self, feature, editWidgetFactory, parent=None):
        """Constructor."""
        QDialog.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.feature = feature
        self.setupUi(self)

        self.editWidget = editWidgetFactory(self.feature, self)
        self.editLayout.addWidget(self.editWidget)

        self.setWindowTitle(f"Edit Feature - {self.feature.TITLE}")
        self.cancelButton.clicked.connect(self.reject)
        self.saveButton.clicked.connect(self.accept)

    def showEvent(self, event):
        super().showEvent(event)

    def accept(self):
        self.workspace.saveEditsAndDerive(self.editWidget.saveFeature)
        super().accept()

    def reject(self):
        self.feature = None
        super().reject()
