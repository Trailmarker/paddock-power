# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from qgis.gui import QgsCollapsibleGroupBox

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_details_group_box_base.ui')))


class FenceDetails(QgsCollapsibleGroupBox, FORM_CLASS):

    def __init__(self, milestone, paddock, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.milestone = milestone
        self.fence = paddock

        self.refreshUi()

    def refreshUi(self):
        """Show the Fence Details."""
        if self.fence is not None:
            self.lengthText.setText(self.fence.featureLength)
