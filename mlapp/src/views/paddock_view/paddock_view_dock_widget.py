# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QDockWidget

from ...models.paddock_power_state import PaddockPowerState

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_view_dock_widget_base.ui')))


class PaddockViewDockWidget(QDockWidget, FORM_CLASS):

    closingDockWidget = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(QDockWidget, self).__init__(parent)

        self.setupUi(self)

        self.state = PaddockPowerState()
        
        self.paddockFilterLineEdit.textChanged.connect(self.onPaddockFilterChanged)
        self.clearPaddockFilterButton.clicked.connect(self.paddockFilterLineEdit.clear)

    def onPaddockFilterChanged(self, text):
        self.paddockList.filterByName(text)

    def showEvent(self, event):
        self.state.detectProject()

    def closeEvent(self, event):
        self.closingDockWidget.emit()
        event.accept()
