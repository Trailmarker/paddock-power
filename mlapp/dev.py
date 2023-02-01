# -*- coding: utf-8 -*-
import os.path as path

from os import mkdir

from qgis.core import QgsProject
from qgis.utils import plugins

from .src.layers.features import MetricPaddock
from .src.layers.features import Waterpoint
from .src.layers.fields.field_map import FieldMap
from .src.layers.land_type_condition_table import LandTypeConditionTable
from .src.layers.derived_boundary_layer import DerivedBoundaryLayer
from .src.layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from .src.layers.derived_paddock_land_types_layer import DerivedPaddockLandTypesLayer
from .src.layers.derived_watered_area_layer import DerivedWateredAreaLayer
from .src.layers.derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from .src.layers.elevation_layer import ElevationLayer
from .src.layers.feature_layer import FeatureLayer
from .src.layers.fence_layer import FenceLayer
from .src.layers.land_type_layer import LandTypeLayer
from .src.layers.paddock_layer import PaddockLayer
from .src.layers.paddock_land_types_layer import PaddockLandTypesLayer
from .src.layers.pipeline_layer import PipelineLayer
from .src.layers.watered_area_layer import WateredAreaLayer
from .src.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from .src.layers.waterpoint_layer import WaterpointLayer
from .src.layers.waterpoint_popup_layer import WaterpointPopupLayer
from .src.layers.metric_paddock_land_types_popup_layer import MetricPaddockCurrentLandTypesPopupLayer, MetricPaddockFutureLandTypesPopupLayer

from .src.utils import resolvePluginPath, qgsDebug, PLUGIN_NAME


def plugin():
    f"""Get the instance of the {PLUGIN_NAME} plug-in"""
    return plugins['mlapp']


def container():
    f"""Get the {PLUGIN_NAME} container."""
    return plugin().container


def workspace():
    f"""Get the current {PLUGIN_NAME} Workspace."""
    return plugin().workspace


def allLayers():
    f"""Get all layers in the current project."""
    return QgsProject.instance().mapLayers().values()


def workspaceLayers():
    f"""Get all layers in the current workspace."""
    return workspace().workspaceLayers


def byType(layerType):
    f"""Get the layer with the given type in the current workspace."""
    return workspace().workspaceLayers.layer(layerType)


def show(layer):
    f"""Show the given layer."""
    QgsProject.instance().layerTreeRoot().addLayer(layer)


def feature(layer, id):
    f"""Get feature by FID in the given layer."""
    return layer.getFeature(id)


def first(layer):
    f"""Get the first feature in the given layer."""
    return next(layer.getFeatures())


def exportStyles(relativeOutDir, overwrite=False):
    f"""Export all FeatureLayer styles to the given directory."""

    outputDir = resolvePluginPath(relativeOutDir)

    if not path.exists(outputDir):
        mkdir(outputDir)

    for layer in [l for l in allLayers() if isinstance(l, FeatureLayer)]:
        if layer.styleName is not None:
            outFile = path.join(outputDir, f"{layer.styleName}.qml")

            if overwrite or not path.exists(outFile):
                layer.saveNamedStyle(outFile)
            else:
                qgsDebug("Can't save style for layer " + layer.name() + " because the file already exists: " + outFile)


layerTypes = [
    LandTypeConditionTable,
    DerivedBoundaryLayer,
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
    WaterpointLayer]


def checkLayers():
    return [byType(layerType) for layerType in layerTypes]


if workspace():
    [conditionTable, derivedBoundaryLayer, derivedMetricPaddockLayer, derivedPaddockLandTypeLayer,
     derivedWateredAreaLayer, derivedWaterpointBufferLayer, elevationLayer,
     fenceLayer, landTypeLayer, paddockLayer, paddockLandTypeLayer, pipelineLayer,
     wateredAreaLayer, waterpointBufferLayer, waterpointLayer] = checkLayers()


# kidmanPaddocks = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == "b_Kidman_Paddocks"), None)
# kidmanLandTypes = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == "c_Kidman_30k_land_units"), None)
# kidmanWaterpoints = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == "a_Kidman_Waterpoints"), None)

# kidmanPaddockFieldMap = FieldMap(kidmanPaddocks, paddocks)
# kidmanLandTypeFieldMap = FieldMap(kidmanLandTypes, landTypes)
# kidmanWaterpointFieldMap = FieldMap(kidmanWaterpoints, waterpoints)


# def testImportKidmanPaddocks():
#     kidmanPaddockFieldMap["Name"] = "Name"
#     paddocks.importFeatures(kidmanPaddocks, kidmanPaddockFieldMap)

# def testImportKidmanLandTypes():
#     kidmanLandTypeFieldMap["LAND_UNIT"] = "Land Type Name"
#     landTypes.importFeatures(kidmanLandTypes, kidmanLandTypeFieldMap)

# def testImportKidmanWaterpoints():
#     kidmanWaterpointFieldMap["NAME"] = "Name"
#     kidmanWaterpointFieldMap["LAYER"] = "Waterpoint Type"
#     waterpoints.importFeatures(kidmanWaterpoints, kidmanWaterpointFieldMap)
