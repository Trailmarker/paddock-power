# -*- coding: utf-8 -*-
import os.path as path

from os import chdir, getcwd, mkdir

from qgis.core import QgsProject
from .src.spatial.layers.elevation_layer import ElevationLayer
from .src.spatial.layers.feature_layer import FeatureLayer
from .src.utils import resolvePluginPath, qgsDebug

def layers():
    return QgsProject.instance().mapLayers().values()


def isFeatureLayer(layer):
    return isinstance(layer, FeatureLayer)


def isPluginLayer(layer):
    return isFeatureLayer(layer) or isinstance(layer, ElevationLayer)


def featureLayers():
    return [layer for layer in layers() if isFeatureLayer(layer)]


def pluginLayers():
    return [layer for layer in layers() if isPluginLayer(layer)]


def notPluginLayers():
    return [layer for layer in layers() if not isPluginLayer(layer)]


def ids():
    return [layer.id() for layer in layers()]


def pluginIds():
    return [layer.id() for layer in pluginLayers()]


def byName(name):
    return next(layer for layer in pluginLayers() if layer.name() == name)


def feature(layer):
    return next(layer.getFeatures())


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


def exportStyles(relativeOutDir, overwrite=False):
    """Export all FeatureLayer styles to the given directory."""
    
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
