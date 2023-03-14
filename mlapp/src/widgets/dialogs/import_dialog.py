# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from .dialog import Dialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'import_dialog_base.ui')))


class ImportDialog(Dialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        Dialog.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

    @property
    def dialogRole(self):
        return "Import"

    def reject(self):
        super().reject()
