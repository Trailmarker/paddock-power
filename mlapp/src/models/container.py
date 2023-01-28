import os.path

from dependency_injector import containers, providers

from qgis.utils import iface

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
from ..utils import PLUGIN_NAME, guiError, guiInformation, qgsInfo, resolveProjectFile, resolveWorkspaceFile


def resolveProjectFileWithWarnings():
    projectFile = resolveProjectFile()
    
    if not projectFile:
        guiError(f"Please create and save a QGIS project before you try to create a {PLUGIN_NAME} Workspace.")
        return None
    return projectFile


def resolveWorkspaceFileWithWarnings(projectFile: str):
    workspaceFile = resolveWorkspaceFile(projectFilePath=projectFile)
    
    if workspaceFile is not None and os.path.exists(workspaceFile):
        guiInformation(f"Found existing {PLUGIN_NAME} Workspace file: {workspaceFile}")
        qgsInfo(f"{PLUGIN_NAME} loading workspace …")
        return workspaceFile
    else:
        return None


class Container(containers.DeclarativeContainer):
    
    projectFile                   = providers.Singleton(resolveProjectFileWithWarnings)
    
    workspaceFile                 = providers.Singleton(resolveWorkspaceFileWithWarnings,
                                                        projectFile = projectFile)
    
    qgisInterface                 = providers.Singleton(lambda: iface)
        
    landTypeLayer                 = providers.Singleton(LandTypeLayer,
                                                        workspaceFile = workspaceFile) 
    
    conditionTable                = providers.Singleton(ConditionTable,
                                                        workspaceFile = workspaceFile)

    elevationLayer                = providers.Singleton(ElevationLayer,
                                                        workspaceFile = workspaceFile)

    paddockLayer                  = providers.Singleton(PaddockLayer,
                                                        workspaceFile = workspaceFile,
                                                        conditionTable = conditionTable)

    waterpointLayer               = providers.Singleton(WaterpointLayer,
                                                        workspaceFile = workspaceFile,
                                                        elevationLayer = elevationLayer)

    derivedWaterpointBufferLayer  = providers.Singleton(DerivedWaterpointBufferLayer,
                                                        workspaceFile = workspaceFile,
                                                        paddockLayer = paddockLayer,
                                                        waterpointLayer = waterpointLayer)

    waterpointBufferLayer         = providers.Singleton(WaterpointBufferLayer,
                                                        workspaceFile = workspaceFile,
                                                        derivedWaterpointBufferLayer = derivedWaterpointBufferLayer)

    derivedWateredAreaLayer       = providers.Singleton(DerivedWateredAreaLayer,
                                                        workspaceFile = workspaceFile,
                                                        paddockLayer = paddockLayer,
                                                        waterpointBufferLayer = waterpointBufferLayer)

    wateredAreaLayer              = providers.Singleton(WateredAreaLayer,
                                                        workspaceFile = workspaceFile,
                                                        derivedWateredAreaLayer = derivedWateredAreaLayer)

    derivedPaddockLandTypesLayer  = providers.Singleton(DerivedPaddockLandTypesLayer,
                                                        workspaceFile = workspaceFile,
                                                        conditionTable = conditionTable,
                                                        paddockLayer = paddockLayer,
                                                        landTypeLayer = landTypeLayer,
                                                        wateredAreaLayer = wateredAreaLayer)

    paddockLandTypesLayer         = providers.Singleton(PaddockLandTypesLayer,
                                                        workspaceFile = workspaceFile,
                                                        derivedPaddockLandTypesLayer = derivedPaddockLandTypesLayer)

    derivedMetricPaddockLayer     = providers.Singleton(DerivedMetricPaddockLayer,
                                                        workspaceFile = workspaceFile,
                                                        conditionTable = conditionTable,
                                                        paddockLayer = paddockLayer,)

    fenceLayer                    = providers.Singleton(FenceLayer,
                                                        workspaceFile = workspaceFile,
                                                        elevationLayer = elevationLayer,
                                                        paddockLayer = paddockLayer,
                                                        derivedMetricPaddockLayer = derivedMetricPaddockLayer)
 
    pipelineLayer                 = providers.Singleton(PipelineLayer,
                                                        workspaceFile = workspaceFile,
                                                        elevationLayer = elevationLayer)
  
    derivedBoundaryLayer          = providers.Singleton(DerivedBoundaryLayer,
                                                        workspaceFile = workspaceFile,
                                                        paddockLayer = paddockLayer)
    
    workspaceLayers               = providers.Singleton(WorkspaceLayers,
                                                        layers = [
                                                            landTypeLayer,
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
    
    workspace                     = providers.Singleton(Workspace,
                                                        # bool,
                                                        iface = qgisInterface,
                                                        workspaceFile = workspaceFile,
                                                        workspaceLayers = workspaceLayers)
                                                      