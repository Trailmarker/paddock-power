# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QCloseEvent
from qgis.PyQt.QtWidgets import QDockWidget

from ..models.glitch import Glitch
from ..utils import PLUGIN_NAME


class ViewBase(QDockWidget):

    closingView = pyqtSignal(type)

    def __init__(self, wprkspace, parent=None):
        """Constructor."""
        super().__init__(parent)

        if not wprkspace:
            raise Glitch(f"{PLUGIN_NAME} views can't be opened without an open Workspace")

        self.workspace = workspace
        self.workspace.workspaceUnloading.connect(lambda: self.closeEvent(QCloseEvent()))

    def closeEvent(self, event):
        self.closingView.emit(type(self))
        event.accept()
