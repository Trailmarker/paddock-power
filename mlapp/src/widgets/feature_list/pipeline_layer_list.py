# -*- coding: utf-8 -*-
from .feature_layer_list import FeatureLayerList
from .feature_list_item import FeatureListItem


class PipelineLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(pipeline): return FeatureListItem(pipeline)

        super().__init__(listItemFactory, parent)

