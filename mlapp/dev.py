# -*- coding: utf-8 -*-
import os.path as path

from os import mkdir

from qgis.core import QgsProject
from qgis.utils import plugins

from .src.spatial.layers.elevation_layer import ElevationLayer
from .src.spatial.layers.feature_layer import FeatureLayer
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
    return next(layer for layer in pluginLayers() if layer.name() == name)


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


layerNames = [
    'Boundary',
    'Derived Paddock Land Types',
    'Derived Watered Areas',
    'Derived Waterpoint Buffers',
    'Elevation Mapping',
    'Fences',
    'Land Types',
    'Paddock Land Types',
    'Paddocks',
    'Paddocks',
    'Pipelines',
    'Watered Areas',
    'Waterpoint Buffers',
    'Waterpoints']

allLayers = [byName(name) for name in layerNames]

[boundary, derivedPaddockLandTypes, derivedWateredAreas, derivedWaterpointBuffers, elevation, fences, landTypes,
 paddockLandTypes, derivedPaddocks, paddocks, pipelines, wateredAreas, waterpointBuffers, waterpoints] = allLayers

conditionTable = project().conditionTable if project() is not None else None
