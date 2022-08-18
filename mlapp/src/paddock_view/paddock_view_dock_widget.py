# -*- coding: utf-8 -*-
import os

from qgis.core import QgsVectorLayerCache, QgsMessageLog
from qgis.gui import QgsAttributeTableFilterModel, QgsAttributeTableModel, QgsAttributeTableView
from qgis.utils import iface
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QComboBox, QLabel, QTableView, QVBoxLayout

from .paddock_table_model import PaddockTableModel
from ..models.project import Project


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_view_dock_widget_base.ui')))


class PaddockViewDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(PaddockViewDockWidget, self).__init__(parent)

        self.setupUi(self)

        self.state = Project()

        # self.state.milestonesUpdated.connect(self.renderMilestoneComboBox)

        # self.verticalLayout = QVBoxLayout()
        self.renderMilestoneComboBox()
        self.milestoneComboBox.currentIndexChanged.connect(
            self.milestoneComboBoxChanged)
        self.state.currentMilestoneChanged.connect(self.renderPaddockTable)

    def renderPaddockTable(self):
        """Show the paddocks of the current milestone."""

        tableModel = PaddockTableModel(self.state.currentMilestone)
        self.tableView.setModel(tableModel)

        # layer = self.milestone.paddockLayer
        # canvas = iface.mapCanvas()

        # self.layerCache = QgsVectorLayerCache(layer, layer.featureCount())
        # self.tableModel = QgsAttributeTableModel(self.layerCache)
        # self.tableModel.loadLayer()

        # self.tableFilterModel = QgsAttributeTableFilterModel(canvas, self.tableModel, parent=self.tableModel)
        # self.tableFilterModel.setFilterMode(QgsAttributeTableFilterModel.ShowAll)
        # self.tableView.setModel(self.tableFilterModel)

    def renderMilestoneComboBox(self):
        """Re-fill milestone combobox based on the state."""
        milestoneNames = [
            milestoneName for milestoneName in self.state.milestones.keys()]
        milestoneNames.sort()
        self.milestoneComboBox.addItems(milestoneNames)
        # self.milestoneComboBox.setCurrentText(self.state.currentMilestone.milestoneName)

    def milestoneComboBoxChanged(self, index):
        """Switch the active milestone."""
        milestoneName = self.milestoneComboBox.itemText(index)
        self.state.setMilestone(milestoneName)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
