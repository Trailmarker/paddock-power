# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QCloseEvent
from qgis.PyQt.QtWidgets import QDockWidget

from ..models.glitch import Glitch
from ..utils import PLUGIN_NAME

class ViewBase(QDockWidget):

    closingView = pyqtSignal(type)

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        if not project:
            raise Glitch(f"{PLUGIN_NAME} views can't be opened without an open Project")

        self.project = project
        self.project.projectUnloading.connect(lambda: self.closeEvent(QCloseEvent()))

    def closeEvent(self, event):
        self.closingView.emit(type(self))
        event.accept()
