# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

from .fenceline_profile_canvas import FencelineProfileCanvas

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fenceline_profile_dialog_base.ui')))


class FencelineProfileDialog(QDialog, FORM_CLASS):
    def __init__(self, fencelineProfile, parent=None):
        """Constructor."""

        super(QDialog, self).__init__(parent)
        self.setupUi(self)

        self.fencelineProfile = fencelineProfile

        fencelineProfileCanvas = FencelineProfileCanvas(self.fencelineProfile)
        self.horizontalLayout.addWidget(fencelineProfileCanvas)

        self.dismissButton.clicked.connect(self.reject)

    def reject(self):
        """Reject the dialog."""
        super(FencelineProfileDialog, self).reject()
