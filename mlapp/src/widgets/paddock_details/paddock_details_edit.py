# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ...layers.features import Edits
from ...models import WorkspaceMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_details_edit_base.ui')))


class PaddockDetailsEdit(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, paddock, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.paddock = paddock
        self.basePaddock = self.paddock.getBasePaddock()
        if self.basePaddock:
            self.nameLineEdit.setText(self.basePaddock.NAME)

    @property
    def paddockLayer(self):
        """Get the Metric Paddock layer."""
        return self.workspace.paddockLayer

    @property
    def basePaddockLayer(self):
        """Get the Paddock layer."""
        return self.workspace.basePaddockLayer

    def saveFeature(self):
        """Save the Paddock Details."""
        self.paddock.NAME = self.nameLineEdit.text()
        edits = Edits.upsert(self.paddock)
        if self.basePaddock:
            self.basePaddock.NAME = self.nameLineEdit.text()
            return Edits.upsert(self.basePaddock).editBefore(edits) # Cheeky?
        else:
            return edits
