# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from .dialog import Dialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'details_dialog_base.ui')))


class DetailsDialog(Dialog, FORM_CLASS):
    """A dialog for editing a feature."""

    def __init__(self, feature, detailsWidgetFactory, parent=None):
        """Constructor."""
        Dialog.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self.feature = feature

        self.detailsWidget = detailsWidgetFactory(self.feature, self)
        self.detailsLayout.addWidget(self.detailsWidget)

        self.setWindowTitle(f"{self.feature.TITLE}")
        self.dismissButton.clicked.connect(self.reject)

    @property
    def dialogRole(self):
        return "Details"

    def reject(self):
        self.feature = None
        super().reject()
