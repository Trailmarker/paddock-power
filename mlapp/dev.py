# -*- coding: utf-8 -*-
import os.path as path

from os import mkdir

from qgis.core import QgsProject
from qgis.utils import plugins

from .src.spatial.fields.field_map import FieldMap
from .src.spatial.layers.boundary_layer import BoundaryLayer
from .src.spatial.layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from .src.spatial.layers.derived_paddock_land_types_layer import DerivedPaddockLandTypesLayer
from .src.spatial.layers.derived_watered_area_layer import DerivedWateredAreaLayer
from .src.spatial.layers.derived_waterpoint_buffer_layer import DerivedWaterpointBufferLayer
from .src.spatial.layers.elevation_layer import ElevationLayer
from .src.spatial.layers.feature_layer import FeatureLayer
from .src.spatial.layers.fence_layer import FenceLayer
from .src.spatial.layers.land_type_layer import LandTypeLayer
from .src.spatial.layers.paddock_layer import PaddockLayer
from .src.spatial.layers.paddock_land_types_layer import PaddockLandTypesLayer
from .src.spatial.layers.pipeline_layer import PipelineLayer
from .src.spatial.layers.watered_area_layer import WateredAreaLayer
from .src.spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from .src.spatial.layers.waterpoint_layer import WaterpointLayer

from .src.utils import resolvePluginPath, qgsDebug, PLUGIN_NAME


def plugin():
    f"""Get the instance of the {PLUGIN_NAME} plug-in"""
    return plugins['mlapp']


def project():
    f"""Get the current {PLUGIN_NAME} Project."""
    return plugin().project


def layers():
    f"""Get all layers in the current project."""
    return QgsProject.instance().mapLayers().values()


def isFeatureLayer(layer):
    f"""Return True if the given layer is a FeatureLayer."""
    return isinstance(layer, FeatureLayer)


def isPluginLayer(layer):
    f"""Return True if the given layer is a FeatureLayer or ElevationLayer."""
    return isFeatureLayer(layer) or isinstance(layer, ElevationLayer)


def featureLayers():
    f"""Get all FeatureLayers in the current project."""
    return [layer for layer in layers() if isFeatureLayer(layer)]


def pluginLayers():
    f"""Get all FeatureLayers and ElevationLayers in the current project."""
    return [layer for layer in layers() if isPluginLayer(layer)]


def notPluginLayers():
    f"""Get all layers in the current project that are not FeatureLayers or ElevationLayers."""
    return [layer for layer in layers() if not isPluginLayer(layer)]


def ids():
    f"""Get the IDs of all layers in the current project."""
    return [layer.id() for layer in layers()]


def pluginIds():
    f"""Get the IDs of all FeatureLayers and ElevationLayers in the current project."""
    return [layer.id() for layer in pluginLayers()]


def byName(name):
    f"""Get the layer with the given name in the current project."""
    return next((layer for layer in pluginLayers() if layer.name() == name), None)


def byType(type):
    f"""Get the layer with the given type in the current project."""
    return next((layer for layer in pluginLayers() if isinstance(layer, type)), None)


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

    for layer in featureLayers():
        if layer.styleName is not None:
            outFile = path.join(outputDir, f"{layer.styleName}.qml")

            if overwrite or not path.exists(outFile):
                layer.saveNamedStyle(outFile)
            else:
                qgsDebug("Can't save style for layer " + layer.name() + " because the file already exists: " + outFile)


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
    WaterpointLayer]


def checkLayers():
    return [byType(layerType) for layerType in layerTypes]


[boundary, derivedMetricPaddocks, derivedPaddockLandTypes, derivedWateredAreas, derivedWaterpointBuffers, elevation,
 fences, landTypes, paddocks, paddockLandTypes, pipelines, wateredAreas, waterpointBuffers, waterpoints] = checkLayers()


conditionTable = project().conditionTable if project() is not None else None


kidmanPaddocks = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == "b_Kidman_Paddocks"), None)
kidmanLandTypes = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == "c_Kidman_30k_land_units"), None)
kidmanWaterpoints = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == "a_Kidman_Waterpoints"), None)

kidmanPaddockFieldMap = FieldMap(kidmanPaddocks, paddocks)
kidmanLandTypeFieldMap = FieldMap(kidmanLandTypes, landTypes)
kidmanWaterpointFieldMap = FieldMap(kidmanWaterpoints, waterpoints)


def testImportKidmanPaddocks():
    kidmanPaddockFieldMap["Name"] = "Name"
    paddocks.importFeatures(kidmanPaddocks, kidmanPaddockFieldMap)

def testImportKidmanLandTypes():
    kidmanLandTypeFieldMap["LAND_UNIT"] = "Land Type Name"
    landTypes.importFeatures(kidmanLandTypes, kidmanLandTypeFieldMap)
    
def testImportKidmanWaterpoints():
    kidmanWaterpointFieldMap["NAME"] = "Name"
    kidmanWaterpointFieldMap["LAYER"] = "Waterpoint Type"
    waterpoints.importFeatures(kidmanWaterpoints, kidmanWaterpointFieldMap)