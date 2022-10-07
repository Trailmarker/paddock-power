# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QSizePolicy

from .infrastructure_profile_canvas import InfrastructureProfileCanvas

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'infrastructure_profile_dialog_base.ui')))


class InfrastructureProfileDialog(QDialog, FORM_CLASS):
    def __init__(self, fencelineProfile, parent=None):
        """Constructor."""

        super(QDialog, self).__init__(parent)
        self.setupUi(self)

        self.fencelineProfile = fencelineProfile
        useMetres = (fencelineProfile.maximumDistance < 1000)

        maximumDistance = fencelineProfile.maximumDistance if useMetres else fencelineProfile.maximumDistance / 1000
        self.elevationStats.setText(
            f"{fencelineProfile.minimumElevation:,.0f} – {fencelineProfile.maximumElevation:,.0f}m (mean {fencelineProfile.meanElevation})")

        if useMetres:
            self.fencelineLength.setText(f"{maximumDistance:,.0f}m")
        else:
            self.fencelineLength.setText(f"{maximumDistance:,.2f}km")

        fencelineProfileCanvas = InfrastructureProfileCanvas(self.fencelineProfile)
        fencelineProfileCanvas.setSizePolicy(QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        self.gridLayout.addWidget(fencelineProfileCanvas, 2, 0, 1, 2)

        # self.horizontalLayout.addWidget(fencelineProfileCanvas)

        # self.dismissButton.clicked.connect(self.reject)

    def reject(self):
        """Reject the dialog."""
        super(InfrastructureProfileDialog, self).reject()
