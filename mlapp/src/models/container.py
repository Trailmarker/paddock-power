from qgis.utils import iface

from ..models.glitch import Glitch
from ..models.workspace import Workspace
from ..models.workspace_layers import WorkspaceLayers
from ..spatial.layers.condition_table import ConditionTable
from ..spatial.layers.derived_boundary_layer import DerivedBoundaryLayer
from ..spatial.layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from ..spatial.layers.derived_paddock_land_types_layer import DerivedPaddockLandTypesLayer
from ..spatial.layers.derived_watered_area_layer import DerivedWateredAreaLayer
from ..spatial.layers.derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.land_type_layer import LandTypeLayer
from ..spatial.layers.paddock_land_types_layer import PaddockLandTypesLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.watered_area_layer import WateredAreaLayer
from ..spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer
from ..utils import PLUGIN_NAME


class Container:

    def __init__(self):
        self.workspaceFile = None
        self.qgisInterface = None
        self.landTypeLayer = None
        self.conditionTable = None
        self.elevationLayer = None
        self.paddockLayer = None
        self.waterpointLayer = None
        self.derivedWaterpointBufferLayer = None
        self.waterpointBufferLayer = None
        self.derivedWateredAreaLayer = None
        self.wateredAreaLayer = None
        self.derivedPaddockLandTypesLayer = None
        self.paddockLandTypesLayer = None
        self.derivedMetricPaddockLayer = None
        self.fenceLayer = None
        self.pipelineLayer = None
        self.derivedBoundaryLayer = None
        self.workspaceLayers = None
        self.workspace = None

    
    def initServices(self, workspaceFile):
        self.workspaceFile = workspaceFile
        self.qgisInterface = iface
        self.landTypeLayer = LandTypeLayer(self.workspaceFile)
        self.conditionTable = ConditionTable(self.workspaceFile)

        self.elevationLayer = ElevationLayer(
            self.workspaceFile)

        self.paddockLayer = PaddockLayer(
            self.workspaceFile,
            self.conditionTable)

        self.waterpointLayer = WaterpointLayer(
            self.workspaceFile,
            self.elevationLayer)

        self.derivedWaterpointBufferLayer = DerivedWaterpointBufferLayer(
            self.paddockLayer,
            self.waterpointLayer)

        self.waterpointBufferLayer = WaterpointBufferLayer(
            self.workspaceFile,
            self.derivedWaterpointBufferLayer)

        self.derivedWateredAreaLayer = DerivedWateredAreaLayer(
            self.paddockLayer,
            self.waterpointBufferLayer)

        self.wateredAreaLayer = WateredAreaLayer(
            self.workspaceFile,
            self.derivedWateredAreaLayer)

        self.derivedPaddockLandTypesLayer = DerivedPaddockLandTypesLayer(
            self.conditionTable,
            self.paddockLayer,
            self.landTypeLayer,
            self.wateredAreaLayer)

        self.paddockLandTypesLayer = PaddockLandTypesLayer(
            self.workspaceFile,
            self.derivedPaddockLandTypesLayer)

        self.derivedMetricPaddockLayer = DerivedMetricPaddockLayer(
            self.paddockLayer,
            self.paddockLandTypesLayer)

        self.fenceLayer = FenceLayer(
            self.workspaceFile)

        self.pipelineLayer = PipelineLayer(
            self.workspaceFile)

        self.derivedBoundaryLayer = DerivedBoundaryLayer(
            self.paddockLayer)

        self.workspaceLayers = WorkspaceLayers(
            *[self.landTypeLayer,
              self.conditionTable,
              self.paddockLayer,
              self.elevationLayer,
              self.waterpointLayer,
              self.derivedWaterpointBufferLayer,
              self.waterpointBufferLayer,
              self.derivedWateredAreaLayer,
              self.wateredAreaLayer,
              self.derivedPaddockLandTypesLayer,
              self.paddockLandTypesLayer,
              self.derivedMetricPaddockLayer,
              self.fenceLayer,
              self.pipelineLayer,
              self.derivedBoundaryLayer])

        self.workspace = Workspace(
            self.qgisInterface,
            self.workspaceFile,
            self.workspaceLayers)
