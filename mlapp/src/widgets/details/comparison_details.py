# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from .details import Details


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'comparison_details_base.ui')))


class ComparisonDetails(QWidget, FORM_CLASS):

    def __init__(self, details, comparison, detailsTitle=None, comparisonTitle=None, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        details.displayMode = Details.DisplayMode.Outer
        self.detailsGroupBox.layout().addWidget(details)
        self.setDetailsTitle(detailsTitle)

        comparison.displayMode = Details.DisplayMode.Outer
        comparison.inverted = True
        self.comparisonGroupBox.layout().addWidget(comparison)
        self.setComparisonTitle(comparisonTitle)

    def setDetailsTitle(self, title):
        self.detailsGroupBox.setTitle(title)

    def setComparisonTitle(self, title):
        self.comparisonGroupBox.setTitle(title)
