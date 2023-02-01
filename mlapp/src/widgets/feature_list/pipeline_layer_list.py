# -*- coding: utf-8 -*-
from .infrastructure_list_item import InfrastructureListItem
from .feature_layer_list import FeatureLayerList


class PipelineLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(pipeline): return InfrastructureListItem(pipeline, parent=parent)

        super().__init__(listItemFactory, parent)

        self.featureLayer = self.workspace.pipelineLayer

