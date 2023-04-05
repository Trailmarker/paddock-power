# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'waterpoint_details_base.ui')))


class WaterpointDetails(QWidget, FORM_CLASS):

    def __init__(self, waterpoint, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)
        self.waterpoint = waterpoint
        self.refreshUi()

    def refreshUi(self):
        if self.waterpoint is not None:
            self.nearGrazingRadiusText.setValues("{0:.0f}", self.waterpoint.NEAR_GRAZING_RADIUS)
            self.farGrazingRadiusText.setValues("{0:.0f}", self.waterpoint.FAR_GRAZING_RADIUS)
            self.waterpointTypeText.setValues("{0}", self.waterpoint.WATERPOINT_TYPE.value)
