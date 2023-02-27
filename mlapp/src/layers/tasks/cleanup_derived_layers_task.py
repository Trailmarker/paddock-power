# -*- coding: utf-8 -*-
from ...layers import DerivedBoundaryLayer, DerivedWaterpointBufferLayer, DerivedMetricPaddockLayer, DerivedPaddockLandTypesLayer, DerivedWateredAreaLayer
from .cleanup_layers_task import CleanupLayersTask


class CleanupDerivedLayersTask(CleanupLayersTask):

    def __init__(self):
        """Input is a correctly ordered batch of layers."""
        super().__init__(
            [DerivedBoundaryLayer,
             DerivedWaterpointBufferLayer,
             DerivedMetricPaddockLayer,
             DerivedPaddockLandTypesLayer,
             DerivedWateredAreaLayer],
            delay=1
        )
