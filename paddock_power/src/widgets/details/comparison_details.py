# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from .details import Details


FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'comparison_details_base.ui')))


class ComparisonDetails(QWidget, FORM_CLASS):

    def __init__(self, details, comparison, detailsTitle=None, comparisonTitle=None, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self.detailsVerticalLayout = QVBoxLayout(self)
        self.detailsVerticalLayout.setSpacing(0)
        self.detailsVerticalLayout.setContentsMargins(0, 1, 0, 0)
        self.detailsGroupBox.setLayout(self.detailsVerticalLayout)
        self.detailsGroupBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        self.comparisonVerticalLayout = QVBoxLayout(self)
        self.comparisonVerticalLayout.setSpacing(0)
        self.comparisonVerticalLayout.setContentsMargins(0, 1, 0, 0)
        self.comparisonGroupBox.setLayout(self.comparisonVerticalLayout)
        self.comparisonGroupBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

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
