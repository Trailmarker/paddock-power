# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QTabWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'feature_tab_widget_base.ui')))


class FeatureTabWidget(QTabWidget, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setupUi(self)
