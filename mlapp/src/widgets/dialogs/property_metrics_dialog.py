# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from ...layers.fields import Timeframe
from ..details import ComparisonDetails, PropertyDetails
from .dialog import Dialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'property_metrics_dialog_base.ui')))


class PropertyMetricsDialog(Dialog, FORM_CLASS):
    """A dialog for editing a feature."""

    def __init__(self, parent=None):
        """Constructor."""
        Dialog.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        currentProperty = next(self.workspace.propertyLayer.getFeaturesByTimeframe(Timeframe.Current), None)
        futureProperty = next(self.workspace.propertyLayer.getFeaturesByTimeframe(Timeframe.Future), None)

        if currentProperty is not None and futureProperty is not None:
            currentPropertyDetails = PropertyDetails(currentProperty, self)
            futurePropertyDetails = PropertyDetails(futureProperty, self)
            
            self.propertyComparisonDetails = ComparisonDetails(currentPropertyDetails, futurePropertyDetails, Timeframe.Current.value, Timeframe.Future.value, self)
            self.detailsLayout.addWidget(self.propertyComparisonDetails) 

        # Get size right and prevent vertical resizing
        self.adjustSize()
        self.setMaximumHeight(self.height())
        self.setMinimumHeight(self.height())

        # Dialog role serves as title
        self.setWindowTitle(None)
        self.dismissButton.clicked.connect(self.reject)

    @property
    def dialogRole(self):
        return "Property Metrics"

