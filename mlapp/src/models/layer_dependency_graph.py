# -*- coding: utf-8 -*-
from ..spatial.layers.condition_table import ConditionTable
from ..spatial.layers.derived_boundary_layer import DerivedBoundaryLayer
from ..spatial.layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from ..spatial.layers.derived_paddock_land_types_layer import DerivedPaddockLandTypesLayer
from ..spatial.layers.derived_watered_area_layer import DerivedWateredAreaLayer
from ..spatial.layers.derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.land_type_layer import LandTypeLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.paddock_land_types_layer import PaddockLandTypesLayer
from ..spatial.layers.persisted_derived_feature_layer import PersistedDerivedFeatureLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.watered_area_layer import WateredAreaLayer
from ..spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer

from .type_dependency_graph import TypeDependencyGraph


class LayerDependencyGraph(TypeDependencyGraph):
    """A bit like a makefile. Describe the dependencies between layers and the order in which they should be built."""

    def __init__(self):
        super().__init__()

        self.addDependencies(LandTypeLayer, [])
        self.addDependencies(ConditionTable, [])
        self.addDependencies(ElevationLayer, [])
        self.addDependencies(PaddockLayer, [ConditionTable])
        self.addDependencies(WaterpointLayer, [ElevationLayer])
        self.addDependencies(DerivedWaterpointBufferLayer, [PaddockLayer, WaterpointLayer])
        self.addDependencies(WaterpointBufferLayer, [DerivedWaterpointBufferLayer])
        self.addDependencies(DerivedWateredAreaLayer, [PaddockLayer, WaterpointBufferLayer])
        self.addDependencies(WateredAreaLayer, [DerivedWateredAreaLayer])
        self.addDependencies(
            DerivedPaddockLandTypesLayer, [
                ConditionTable, PaddockLayer, LandTypeLayer, WateredAreaLayer])
        self.addDependencies(PaddockLandTypesLayer, [DerivedPaddockLandTypesLayer])
        self.addDependencies(DerivedMetricPaddockLayer, [PaddockLayer, PaddockLandTypesLayer])
        self.addDependencies(FenceLayer, [ElevationLayer, PaddockLayer, DerivedMetricPaddockLayer])
        self.addDependencies(PipelineLayer, [ElevationLayer])
        self.addDependencies(DerivedBoundaryLayer, [PaddockLayer])

    def loadOrder(self):
        """Return a list of layer types in the order they should be initialised."""
        return self.sort()

    def unloadOrder(self):
        """Return a list of layer types in the order they should be unloaded."""
        return list(reversed(self.loadOrder()))
    
    def updateOrder(self, updatedLayers):
        """Return a list of layers that must be 'repersisted' in response to feature updates."""
        updatedLayerTypeNames = [type(layer).__name__ for layer in updatedLayers]
        
        # We don't update anything that isn't affected by a change
        # We 'repersist' all downstream derived layers that are affected
        loadOrder = self.loadOrder()
        
        for i in range(0, len(loadOrder)):
            layerType = loadOrder[i]
            if layerType.__name__ in updatedLayerTypeNames:
                return [t for t in loadOrder[i:] if issubclass(t, PersistedDerivedFeatureLayer)] 
                
        return []
        