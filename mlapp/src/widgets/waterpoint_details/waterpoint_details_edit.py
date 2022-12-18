# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ...spatial.schemas.waterpoint_type import WaterpointType

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'waterpoint_details_edit_base.ui')))


class WaterpointDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, waterpoint, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.waterpoint = waterpoint
        self._waterpointType = waterpoint.waterpointType

        for waterpointType in WaterpointType:
            self.waterpointTypeComboBox.addItem(waterpointType.value, waterpointType)

        self.waterpointTypeComboBox.setCurrentIndex(
            self.waterpointTypeComboBox.findData(self._waterpointType))

        self.waterpointTypeComboBox.currentIndexChanged.connect(self.setWaterpointType)

    @pyqtSlot(int)
    def setWaterpointType(self, index):
        self._waterpointType = self.waterpointTypeComboBox.itemData(index)

    @pyqtSlot()
    def saveFeature(self):
        """Save the Waterpoint, updating the Waterpoint Type."""
        self.waterpoint.waterpointType = self._waterpointType
