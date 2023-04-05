# -*- coding: utf-8 -*-
from ....models import WorkspaceMixin
from ..comparison_details import ComparisonDetails
from ..details import Details


class PaddockComparisonDetails(WorkspaceMixin, ComparisonDetails):

    def __init__(self, details, comparison, detailsTitle=None, comparisonTitle=None, parent=None):
        """Constructor."""
        WorkspaceMixin.__init__(self)

        ComparisonDetails.__init__(self)

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
