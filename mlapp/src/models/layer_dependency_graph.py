# -*- coding: utf-8 -*-
from ..layers.interfaces import IPersistedDerivedFeatureLayer, IPersistedFeatureLayer

from ..layers import *
from .type_dependency_graph import TypeDependencyGraph


class LayerDependencyGraph(TypeDependencyGraph):
    """A bit like a makefile. Describe the dependencies between layers and the order in which they should be built."""

    def __init__(self):
        super().__init__()

        self.addDependencies(LandTypeLayer, [])
        self.addDependencies(LandTypeConditionTable, [])
        self.addDependencies(ElevationLayer, [])
        self.addDependencies(BasePaddockLayer, [])
        self.addDependencies(AnalyticPaddockLayer, [BasePaddockLayer])
        self.addDependencies(WaterpointLayer, [ElevationLayer])
        self.addDependencies(WaterpointBufferLayer, [AnalyticPaddockLayer, WaterpointLayer])
        self.addDependencies(WateredAreaLayer, [AnalyticPaddockLayer, WaterpointBufferLayer])
        self.addDependencies(PaddockLandTypesLayer, [LandTypeConditionTable,
                             AnalyticPaddockLayer, LandTypeLayer, WateredAreaLayer])
        self.addDependencies(PaddockLayer, [AnalyticPaddockLayer, PaddockLandTypesLayer])
        self.addDependencies(FenceLayer, [ElevationLayer, AnalyticPaddockLayer, PaddockLayer])
        self.addDependencies(PipelineLayer, [ElevationLayer])
        self.addDependencies(PropertyLayer, [PaddockLayer])

    def loadOrder(self):
        """Return a list of layer types in the order they should be initialised."""
        return self.sort()

    def unloadOrder(self):
        """Return a list of layer types in the order they should be unloaded."""
        return list(reversed(self.loadOrder()))

    def operationOrder(self, typePredicate, layerTypes=None):
        """Return an order list of layers that must be operated on based on a predicate."""

        # We don't update anything that isn't affected by a change
        # We 'repersist' all the downstream derived layers that are affected
        loadOrder = self.loadOrder()
        layerTypeNames = [t.__name__ for t in (layerTypes or loadOrder)]

        # Return the full load order of types that subclass the provided layerType
        for i in range(0, len(loadOrder)):
            lt = loadOrder[i]
            if lt.__name__ in layerTypeNames:
                return [t for t in loadOrder[i:] if typePredicate(t)]

        return []

    def deriveOrder(self, updatedLayerTypes=None):
        updatedLayerTypes = updatedLayerTypes or self.loadOrder()
        return self.operationOrder(lambda t: issubclass(t, IPersistedDerivedFeatureLayer), updatedLayerTypes)

    def recalculateOrder(self):
        return self.operationOrder(lambda t: issubclass(t, IPersistedFeatureLayer)
                                   and not issubclass(t, IPersistedDerivedFeatureLayer), self.loadOrder())

    def cleanupOrder(self):
        return [PaddockCurrentLandTypesPopupLayer,
                PaddockFutureLandTypesPopupLayer,
                WaterpointBufferPopupLayer,
                PropertyLayer,
                DerivedPropertyLayer,
                PipelineLayer,
                FenceLayer,
                PaddockLayer,
                DerivedMetricPaddockLayer,
                PaddockLandTypesLayer,
                DerivedPaddockLandTypesLayer,
                WateredAreaLayer,
                DerivedWateredAreaLayer,
                WaterpointBufferLayer,
                DerivedWaterpointBufferLayer,
                WaterpointLayer,
                BasePaddockLayer,
                LandTypeLayer,
                ElevationLayer]
        # LandTypeConditionTable]

    def displayOrder(self):
        return [WaterpointLayer,
                PipelineLayer,
                FenceLayer,
                WateredAreaLayer,
                LandTypeLayer,
                PropertyLayer,
                PaddockLayer,
                ElevationLayer]
