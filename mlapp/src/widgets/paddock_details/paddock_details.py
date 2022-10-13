# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_details_base.ui')))


class PaddockDetails(QWidget, FORM_CLASS):

    def __init__(self, paddock, parent=None):
        """Constructor."""
        super(QWidget, self).__init__(parent)

        self.setupUi(self)

        self.paddock = paddock
        if self.paddock is not None:
            self.areaText.setText(str(self.paddock.featureArea()))
            self.perimeterText.setText(str(self.paddock.featurePerimeter()))
            # self.conditionText.setText("Not yet implemented")
