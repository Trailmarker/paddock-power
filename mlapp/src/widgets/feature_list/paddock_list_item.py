# -*- coding: utf-8 -*-
from ..paddock_details.paddock_details import PaddockDetails
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit
from .feature_list_item import FeatureListItem


class PaddockListItem(FeatureListItem):

    def __init__(self, paddock, parent=None):

        super().__init__(
            paddock,
            detailsWidgetFactory=PaddockDetails,
            editWidgetFactory=self.makeEditWidget,
            parent=parent)

    def makeEditWidget(self, paddock):
        """Create a new edit widget for the given Metric Paddock, that will save edits to the corresponding 'underlying' Paddock."""
        editWidget = PaddockDetailsEdit(paddock)

        return editWidget
