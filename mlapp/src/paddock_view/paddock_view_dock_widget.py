# -*- coding: utf-8 -*-
import os

from qgis.core import QgsVectorLayerCache, QgsMessageLog
from qgis.gui import QgsAttributeTableFilterModel, QgsAttributeTableModel, QgsAttributeTableView
from qgis.utils import iface
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QComboBox, QLabel, QTableView, QVBoxLayout

from .paddock_table_model import PaddockTableModel
from ..models.state import getState, getProject
from ..utils import qgsDebug

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_view_dock_widget_base.ui')))


class PaddockViewDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()
    renderNeeded = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(PaddockViewDockWidget, self).__init__(parent)

        self.setupUi(self)

        getState().projectChanged.connect(self.setup)
        getState().projectChanged.connect(self.render)
        self.milestoneComboBox.currentIndexChanged.connect(
            self.milestoneComboBoxChanged)

        self.renderNeeded.connect(self.render)

        self.render()

    def setup(self):
        """Reconnect things as necessary."""
        project = getProject()
        if project is not None:
            project.currentMilestoneChanged.connect(self.render)

    def render(self):
        """Show the Paddock View."""

        project = getState().project
        
        self.milestoneComboBox.blockSignals(True)

        if project is None:
            self.milestoneComboBox.clear()
            self.tableView.setModel(PaddockTableModel(None))
            return

        self.milestoneComboBox.clear()
        milestoneNames = [milestoneName for milestoneName in project.milestones.keys()]
        milestoneNames.sort()
        milestoneNames.insert(0,'')
        self.milestoneComboBox.addItems(milestoneNames)

        if project.currentMilestone is not None:
            self.milestoneComboBox.setCurrentText(project.currentMilestone.milestoneName)
            tableModel = PaddockTableModel(project.currentMilestone.paddockLayer)
            self.tableView.setModel(tableModel)

        self.milestoneComboBox.blockSignals(False)


    def milestoneComboBoxChanged(self, index):
        """Switch the active milestone."""
        milestoneName = self.milestoneComboBox.itemText(index)
        if milestoneName:
            getState().project.setMilestone(milestoneName)
        self.renderNeeded.emit()


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
