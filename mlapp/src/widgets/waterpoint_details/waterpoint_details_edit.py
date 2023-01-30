# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget

from ...spatial.features.edits import Edits
from ...spatial.features.waterpoint import Waterpoint
from ...spatial.fields.waterpoint_type import WaterpointType

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'waterpoint_details_edit_base.ui')))


class WaterpointDetailsEdit(QWidget, FORM_CLASS):

    def __init__(self, waterpoint, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)

        self.waterpoint = waterpoint

        self.nameLineEdit.setText(self.waterpoint.NAME)

        self.nearGrazingRadiusSpinBox.setMinimum(Waterpoint.NEAREST_GRAZING_RADIUS)
        self.nearGrazingRadiusSpinBox.setMaximum(Waterpoint.FARTHEST_GRAZING_RADIUS)
        self.farGrazingRadiusSpinBox.setMinimum(Waterpoint.NEAREST_GRAZING_RADIUS)
        self.farGrazingRadiusSpinBox.setMaximum(Waterpoint.FARTHEST_GRAZING_RADIUS)

        self.nearGrazingRadiusSpinBox.setValue(int(self.waterpoint.NEAR_GRAZING_RADIUS))
        self.farGrazingRadiusSpinBox.setValue(int(self.waterpoint.FAR_GRAZING_RADIUS))

        self.nearGrazingRadiusSpinBox.valueChanged.connect(self.adjustMinimumFarGrazingRadius)
        self.farGrazingRadiusSpinBox.valueChanged.connect(self.adjustMaximumNearGrazingRadius)

        self.adjustMinimumFarGrazingRadius()
        self.adjustMaximumNearGrazingRadius()

        self._waterpointType = waterpoint.WATERPOINT_TYPE

        for waterpointType in WaterpointType:
            self.waterpointTypeComboBox.addItem(waterpointType.value, waterpointType)

        self.waterpointTypeComboBox.setCurrentIndex(
            self.waterpointTypeComboBox.findData(self._waterpointType))

        self.waterpointTypeComboBox.currentIndexChanged.connect(self.setWaterpointType)

    @pyqtSlot()
    def adjustMinimumFarGrazingRadius(self):
        self.farGrazingRadiusSpinBox.setMinimum(
            max(Waterpoint.NEAREST_GRAZING_RADIUS, self.nearGrazingRadiusSpinBox.value()))

    @pyqtSlot()
    def adjustMaximumNearGrazingRadius(self):
        self.nearGrazingRadiusSpinBox.setMaximum(
            min(Waterpoint.FARTHEST_GRAZING_RADIUS, self.farGrazingRadiusSpinBox.value()))

    @pyqtSlot(int)
    def setWaterpointType(self, index):
        self._waterpointType = self.waterpointTypeComboBox.itemData(index)

    def saveFeature(self):
        """Save the Waterpoint, updating the Waterpoint Type."""

        self.waterpoint.NAME = self.nameLineEdit.text()
        self.waterpoint.WATERPOINT_TYPE = self._waterpointType
        self.waterpoint.NEAR_GRAZING_RADIUS = float(self.nearGrazingRadiusSpinBox.value())
        self.waterpoint.FAR_GRAZING_RADIUS = float(self.farGrazingRadiusSpinBox.value())
        
        return Edits.upsert(self.waterpoint)
