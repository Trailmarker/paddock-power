from dependency_injector import containers, providers

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
from ..utils import PLUGIN_NAME, resolveProjectFile, resolveWorkspaceFile


def resolveWorkspaceFileOrFail(projectFile: str):
    workspaceFile = resolveWorkspaceFile(projectFilePath=projectFile)
    if workspaceFile is None:
        raise Glitch(f"Could not resolve {PLUGIN_NAME} workspace file.")
    return workspaceFile


class Container(containers.DeclarativeContainer):

    projectFile = providers.Factory(resolveProjectFile)

    workspaceFile = providers.Factory(resolveWorkspaceFileOrFail,
                                      projectFile)

    qgisInterface = providers.Singleton(lambda: iface)

    landTypeLayer = providers.Singleton(LandTypeLayer,
                                        workspaceFile)

    conditionTable = providers.Singleton(ConditionTable,
                                         workspaceFile)

    elevationLayer = providers.Singleton(ElevationLayer,
                                         workspaceFile)

    paddockLayer = providers.Singleton(PaddockLayer,
                                       workspaceFile,
                                       conditionTable)

    waterpointLayer = providers.Singleton(WaterpointLayer,
                                          workspaceFile,
                                          elevationLayer)

    derivedWaterpointBufferLayer = providers.Singleton(DerivedWaterpointBufferLayer,
                                                       paddockLayer,
                                                       waterpointLayer)

    waterpointBufferLayer = providers.Singleton(WaterpointBufferLayer,
                                                workspaceFile,
                                                derivedWaterpointBufferLayer)

    derivedWateredAreaLayer = providers.Singleton(DerivedWateredAreaLayer,
                                                  paddockLayer,
                                                  waterpointBufferLayer)

    wateredAreaLayer = providers.Singleton(WateredAreaLayer,
                                           workspaceFile,
                                           derivedWateredAreaLayer)

    derivedPaddockLandTypesLayer = providers.Singleton(DerivedPaddockLandTypesLayer,
                                                       conditionTable,
                                                       paddockLayer,
                                                       landTypeLayer,
                                                       wateredAreaLayer)

    paddockLandTypesLayer = providers.Singleton(PaddockLandTypesLayer,
                                                workspaceFile,
                                                derivedPaddockLandTypesLayer)

    derivedMetricPaddockLayer = providers.Singleton(DerivedMetricPaddockLayer,
                                                    paddockLayer,
                                                    paddockLandTypesLayer)

    fenceLayer = providers.Singleton(FenceLayer,
                                     workspaceFile)

    pipelineLayer = providers.Singleton(PipelineLayer,
                                        workspaceFile)

    derivedBoundaryLayer = providers.Singleton(DerivedBoundaryLayer,
                                               paddockLayer)

    workspaceLayers = providers.Singleton(WorkspaceLayers,
                                          *[landTypeLayer,
                                            conditionTable,
                                            paddockLayer,
                                            elevationLayer,
                                            waterpointLayer,
                                            derivedWaterpointBufferLayer,
                                            waterpointBufferLayer,
                                            derivedWateredAreaLayer,
                                            wateredAreaLayer,
                                            derivedPaddockLandTypesLayer,
                                            paddockLandTypesLayer,
                                            derivedMetricPaddockLayer,
                                            fenceLayer,
                                            pipelineLayer,
                                            derivedBoundaryLayer])

    workspace = providers.Singleton(Workspace,
                                    qgisInterface,
                                    workspaceFile,
                                    workspaceLayers)
