# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon

from qgis.gui import QgsCollapsibleGroupBox

from ...utils import guiConfirm, qgsDebug

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'fence_details_group_box_base.ui')))


class FenceDetails(QgsCollapsibleGroupBox, FORM_CLASS):

    NAME, AREA, PERIMETER = ["Paddock Name", "Paddock Area (km²)", "Paddock Perimeter (km)"]
    
    refreshUiNeeded = pyqtSignal()

    def __init__(self, milestone, paddock, parent=None):
        """Constructor."""
        super(QgsCollapsibleGroupBox, self).__init__(parent)

        self.setupUi(self)

        self.milestone = milestone
        self.paddock = paddock
        
        self.refreshUiNeeded.connect(self.refreshUi)
        self.refreshUi()

    def refreshUi(self):
        """Show the Paddock Details."""
        if self.paddock is not None:
            self.setTitle(self.paddock[self.NAME]) # QGroupBox function

            self.nameText.setText(self.paddock[self.NAME])
            self.areaText.setText(self.paddock[self.AREA])
            self.perimeterText.setText(self.paddock[self.PERIMETER])

            self.conditionComboBox.addItem("Not implemented yet")


