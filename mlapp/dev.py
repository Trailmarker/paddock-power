# -*- coding: utf-8 -*-
import os.path as path

from os import mkdir

from qgis.core import QgsProject
from qgis.utils import plugins

from .src.layers.fields import Timeframe, FeatureStatus
from .src.layers.features import *
from .src.layers.interfaces import *
from .src.layers.tasks import *
from .src.layers import *


from .src.utils import resolvePluginPath, qgsDebug, PLUGIN_FOLDER, PLUGIN_NAME


def plugin():
    f"""Get the instance of the {PLUGIN_NAME} plug-in"""
    return plugins[PLUGIN_FOLDER]


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

    for layer in [l for l in allLayers() if isinstance(l, IFeatureLayer)]:
        if layer.styleName is not None:
            outFile = path.join(outputDir, f"{layer.styleName}.qml")

            if overwrite or not path.exists(outFile):
                layer.saveNamedStyle(outFile)
            else:
                qgsDebug("Can't save style for layer " + layer.name() + " because the file already exists: " + outFile)


layerTypes = [
    LandTypeConditionTable,
    BoundaryLayer,
    PaddockLayer,
    ElevationLayer,
    FenceLayer,
    LandTypeLayer,
    BasePaddockLayer,
    PaddockLandTypesLayer,
    PipelineLayer,
    WateredAreaLayer,
    WaterpointBufferLayer,
    WaterpointLayer]


def checkLayers():
    return [byType(layerType) for layerType in layerTypes]


if workspace():
    [landTypeConditionTable, boundaryLayer, paddockLayer,
     elevationLayer, fenceLayer, landTypeLayer,
     basePaddockLayer, paddockLandTypeLayer, pipelineLayer,
     wateredAreaLayer, waterpointBufferLayer, waterpointLayer] = checkLayers()
    
fv = plugin().featureView
paddockTableView = fv.paddockTab.paddockTableView
pipelineTableView = fv.pipelineTab.pipelineTableView
fenceTableView = fv.fenceTab.fenceTableView
waterpointTableView = fv.waterpointTab.waterpointTableView
