# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'import_dialog_base.ui')))


class ImportDialog(QDialog, FORM_CLASS):
    def __init__(self, plugin, parent=None):
        """Constructor."""
        QDialog.__init__(self, parent)
        FORM_CLASS.__init__(self)
     
        self.setupUi(self)

        self.plugin = plugin
        
        
    # def closeEvent(self, event):
    #     self.
    #     event.accept()