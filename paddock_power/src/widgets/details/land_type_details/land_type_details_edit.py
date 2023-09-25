# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ....layers.features import Edits, LandType
from ....models import WorkspaceMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'land_type_details_edit_base.ui')))


class LandTypeDetailsEdit(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, landType, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.optimalCapacityPerAreaDoubleSpinBox.setMinimum(LandType.MINIMUM_OPTIMAL_CAPACITY_PER_AREA)
        self.optimalCapacityPerAreaDoubleSpinBox.setMaximum(LandType.MAXIMUM_OPTIMAL_CAPACITY_PER_AREA)

        self.landType = landType
        self.landTypeNameLineEdit.setText(self.landType.LAND_TYPE_NAME)
        self.optimalCapacityPerAreaDoubleSpinBox.setValue(self.landType.OPTIMAL_CAPACITY_PER_AREA)

    def saveFeature(self):
        """Save the Land Type Details."""
        self.landType.LAND_TYPE_NAME = self.landTypeNameLineEdit.text()
        self.landType.OPTIMAL_CAPACITY_PER_AREA = self.optimalCapacityPerAreaDoubleSpinBox.value()
        return Edits.upsert(self.landType)
