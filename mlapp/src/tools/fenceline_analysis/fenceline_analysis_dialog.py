# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

from .fenceline_analysis_canvas import FencelineAnalysisCanvas

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fenceline_analysis_dialog_base.ui')))


class FencelineAnalysisDialog(QDialog, FORM_CLASS):
    def __init__(self, splitPaddockTool, parent=None):
        """Constructor."""

        super(QDialog, self).__init__(parent)
        self.setupUi(self)

        figure = FencelineAnalysisCanvas(self, width=5, height=4, dpi=100)
        figure.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        self.horizontalLayout.addWidget(figure)

        self.dismissButton.clicked.connect(self.reject)

    def reject(self):
        """Reject the dialog."""
        super(FencelineAnalysisDialog, self).reject()

