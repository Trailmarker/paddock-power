# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ....layers.features import Edits

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_details_edit_base.ui')))


class FenceDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, fence, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self.fence = fence
        if self.fence:
            self.nameLineEdit.setText(self.fence.NAME)

    def saveFeature(self):
        """Save the Paddock Details."""
        self.fence.NAME = self.nameLineEdit.text()
        return Edits.upsert(self.fence)
