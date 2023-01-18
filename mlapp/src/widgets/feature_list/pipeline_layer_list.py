# -*- coding: utf-8 -*-
from .infrastructure_list_item import InfrastructureListItem
from .persisted_feature_layer_list import PersistedFeatureLayerList


class PipelineLayerList(PersistedFeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(pipeline): return InfrastructureListItem(pipeline, parent=parent)

        super().__init__(listItemFactory, parent)
