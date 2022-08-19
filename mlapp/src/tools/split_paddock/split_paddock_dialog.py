# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'split_paddock_dialog_base.ui')))

class SplitPaddockDialog(QDialog, FORM_CLASS):
    def __init__(self, splitPaddockTool, parent=None):
        """Constructor."""

        super(QDialog, self).__init__(parent)
        self.setupUi(self)

        self.splitPaddockTool = splitPaddockTool

        self.cancelSplitButton.clicked.connect(self.reject)
        self.confirmSplitButton.clicked.connect(self.accept)

    def setFenceLength(self, length):
        """Set the fence length."""
        self.fenceLengthText.setText(f"{length:,.0f}")

    def reject(self):
        """Reject the dialog."""
        self.splitPaddockTool.finishSplitPaddocks()
        super(SplitPaddockDialog, self).reject()

    def accept(self):
        """Accept the dialog."""
        self.splitPaddockTool.splitPaddocks()
        super(SplitPaddockDialog, self).accept()