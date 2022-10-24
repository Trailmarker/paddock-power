# -*- coding: utf-8 -*-
from ..feature_list.feature_layer_list import FeatureLayerList
from ..feature_list.feature_list_item import FeatureListItem


class FenceLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(fence): return FeatureListItem(fence)

        super().__init__(listItemFactory, parent)

    def setProject(self, project):
        """Set the FeatureLayer."""
        self.featureLayer = project.fenceLayer
        self.featureLayer.editsPersisted.connect(self.refreshUi)
        super().setProject(project)
