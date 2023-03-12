# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

from ...models import WorkspaceMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'details_dialog_base.ui')))


class DetailsDialog(QDialog, FORM_CLASS, WorkspaceMixin):
    """A dialog for editing a feature."""

    def __init__(self, feature, detailsWidgetFactory, parent=None):
        """Constructor."""
        QDialog.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.feature = feature
        self.setupUi(self)

        self.detailsWidget = detailsWidgetFactory(self.feature, self)
        self.detailsLayout.addWidget(self.detailsWidget)

        self.setWindowTitle(f"Feature - {self.feature.TITLE}")
        self.cancelButton.clicked.connect(self.reject)

    def showEvent(self, event):
        super().showEvent(event)

    def reject(self):
        self.feature = None
        super().reject()
