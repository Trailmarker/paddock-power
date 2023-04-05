# -*- coding: utf-8 -*-
from ....layers.fields import Timeframe
from ..comparison_details import ComparisonDetails
from .property_details import PropertyDetails

class PropertyComparisonDetails(ComparisonDetails):

    def __init__(self, currentProperty, futureProperty, parent=None):
        """Constructor."""
        currentPropertyDetails = PropertyDetails(currentProperty, self)
        futurePropertyDetails = PropertyDetails(futureProperty, self)
        
        ComparisonDetails.__init__(self, currentPropertyDetails, futurePropertyDetails, Timeframe.Current.value, Timeframe.Future.value, parent)
