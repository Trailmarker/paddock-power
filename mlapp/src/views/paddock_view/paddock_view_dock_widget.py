# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QDockWidget

from ...models.state import detectProject

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_view_dock_widget_base.ui')))


class PaddockViewDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(QDockWidget, self).__init__(parent)

        self.setupUi(self)

        # test filtering stuff
        # self.paddockList.filterByName("Test")

    def showEvent(self, event):
        detectProject()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
