# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QObject

from qgis.core import QgsProject

from ..spatial.features.fence import Fence
from ..spatial.features.paddock import Paddock
from ..spatial.features.waterpoint import Waterpoint
from ..spatial.layers.condition_table import ConditionTable
from ..spatial.layers.boundary_layer import BoundaryLayer
from ..spatial.layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from ..spatial.layers.derived_paddock_land_types_layer import DerivedPaddockLandTypesLayer
from ..spatial.layers.derived_watered_area_layer import DerivedWateredAreaLayer
from ..spatial.layers.derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.land_type_layer import LandTypeLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.paddock_land_types_layer import PaddockLandTypesLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.watered_area_layer import WateredAreaLayer
from ..spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer
from .workspace_layers_unused import WorkspaceLayers
from ..utils import PLUGIN_NAME, resolveGeoPackageFile, qgsDebug
from .type_dependency_graph import TypeDependencyGraph

class WorkspaceBase(QObject):

    layerTypes = [
        BoundaryLayer,
        DerivedMetricPaddockLayer,
        DerivedPaddockLandTypesLayer,
        DerivedWateredAreaLayer,
        DerivedWaterpointBufferLayer,
        ElevationLayer,
        FenceLayer,
        LandTypeLayer,
        PaddockLayer,
        PaddockLandTypesLayer,
        PipelineLayer,
        WateredAreaLayer,
        WaterpointBufferLayer,
        WaterpointLayer
    ]

    def __init__(self, gpkgFile=None, workspaceName=None):
        super().__init__()

        gpkgFile = gpkgFile or resolveGeoPackageFile()
        self.gpkgFile = gpkgFile
        self.workspaceName = workspaceName or PLUGIN_NAME

        self._dependencyGraph = TypeDependencyGraph(typeFactory=lambda cls: self._layers[cls])

        self._dependencyGraph.addDependencies(BoundaryLayer, [PaddockLayer])
        self._dependencyGraph.addDependencies(ConditionTable, [])
        self._dependencyGraph.addDependencies(DerivedMetricPaddockLayer, [ConditionTable, PaddockLayer, PaddockLandTypesLayer])
        self._dependencyGraph.addDependencies(DerivedPaddockLandTypesLayer, [ConditionTable, PaddockLayer, LandTypeLayer, WateredAreaLayer])
        self._dependencyGraph.addDependencies(DerivedWateredAreaLayer, [PaddockLayer, WaterpointBufferLayer])
        self._dependencyGraph.addDependencies(DerivedWaterpointBufferLayer, [PaddockLayer, WaterpointLayer])
        self._dependencyGraph.addDependencies(FenceLayer, [])
        self._dependencyGraph.addDependencies(LandTypeLayer, [])
        self._dependencyGraph.addDependencies(PaddockLayer, [])
        self._dependencyGraph.addDependencies(PipelineLayer, [])
        self._dependencyGraph.addDependencies(PaddockLandTypesLayer, [DerivedPaddockLandTypesLayer])
        self._dependencyGraph.addDependencies(WaterpointLayer, [])
        self._dependencyGraph.addDependencies(WaterpointBufferLayer, [DerivedWaterpointBufferLayer])
        self._dependencyGraph.addDependencies(WateredAreaLayer, [DerivedWateredAreaLayer])
    
        self._referenceGraph = TypeDependencyGraph(typeFactory=lambda cls: self._layers[cls])
        self._referenceGraph.addDependencies(Fence, [DerivedMetricPaddockLayer, PaddockLayer])
        self._referenceGraph.addDependencies(Paddock, [ConditionTable])
        self._referenceGraph.addDependencies(Waterpoint, [WaterpointBufferLayer])
        
        self._layers = WorkspaceLayers()

        elevationLayerName = ElevationLayer.detectInGeoPackage(self.gpkgFile)
        if elevationLayerName is not None:
            self.elevationLayer = ElevationLayer(self, self.gpkgFile, elevationLayerName)
        else:
            self.elevationLayer = None

        # Sort all the layer types in type dependency order
        dependencyOrderedLayerTypes = self._dependencyGraph.topologicalSort()

        qgsDebug(f"Layer types in dependency order: {str([t.__name__ for t in dependencyOrderedLayerTypes])}")

        # Create all layers in dependency order
        for layerType in dependencyOrderedLayerTypes:
            if layerType is ElevationLayer:
                continue
            qgsDebug(f"Creating layer of type {layerType.__name__}")
            # referencedLayers=self.referencedLayers(layerType)
            self._layers[layerType] = layerType(self, dependentLayers=self.dependentLayers(layerType))


    def dependentLayerTypes(self, obj):
        """Return a list of layer types on which the given layer or type depends."""       
        return self._dependencyGraph.getDependencies(obj)
    
    def referencedLayerTypes(self, obj):
        """Return a list of layer types to which the given layer refers."""
        return self._dependencyGraph.getDependencies(obj)

    def dependentLayers(self, layer):
        """Return a list of layers on which the given layer depends."""
        return dict([(layerType, self._layers[layerType]) for layerType in self.dependentLayerTypes(layer)])

    def referencedLayers(self, feature):
        """Return a list of layers to which the given layer refers."""
        return dict([(layerType, self._layers[layerType]) for layerType in self.referencedLayerTypes(feature)])

    def layerByType(self, layerType):
        """Return a layer of a type on which the given layer depends."""
        return self._layers[layerType]

    def findGroup(self):
        """Find this Project's group in the Layers panel."""
        group = QgsProject.instance().layerTreeRoot().findGroup(self.workspaceName)
        if group is None:
            group = QgsProject.instance().layerTreeRoot().insertGroup(0, self.workspaceName)
        return group

    def addToMap(self, group=None):
        """Add this Project to the map."""
        self.removeFromMap()

        group = group or self.findGroup()
        
        # for layerType in [WaterpointLayer, PipelineLayer, FenceLayer, WateredAreaLayer, LandTypeLayer, DerivedBoundaryLayer, DerivedMetricPaddockLayer]:
        #     self._layers[layerType].addToMap(group)

        if self.elevationLayer is not None:
            self.elevationLayer.addToMap(group)

    def removeFromMap(self):
        """Remove this Project from the current map view."""
        group = self.findGroup()
        QgsProject.instance().layerTreeRoot().removeChildNode(group)
