# -*- coding: utf-8 -*-
from qgis.core import QgsMapLayer, QgsProject

from ..layers.interfaces import IFeatureLayer, ILayer
from ..utils import PLUGIN_NAME
from .glitch import Glitch
from .type_dict import TypeDict


class WorkspaceLayers(TypeDict):
    def __init__(self, *layers):
        f"""Create a type registry for {PLUGIN_NAME}'s Layer like objects."""
        super().__init__()

        for layer in layers:
            self.addLayer(type(layer), layer)

    def addObject(self, layerType, object):
        raise NotImplementedError("Use addLayer instead")

    def getObject(self, layerType):
        raise NotImplementedError("Use layer instead")

    def addLayer(self, layerType, layer):
        """Add a layer to the registry."""
        if not isinstance(layer, ILayer):
            raise Glitch(f"Invalid WorkspaceLayers value: must be an ILayer")

        super().addObject(layerType, layer)

    def layer(self, layerType):
        """Get the layer for the given layer type."""
        return super().getObject(layerType)

    def layers(self):
        """Get all layers in the registry."""
        return list(map(self.valueToObject, self.values()))

    def featureLayers(self):
        """Get all layers in the registry."""
        return [l for l in self.layers() if isinstance(l, IFeatureLayer)]

    def addLayersToWorkspace(self, workspace):
        """Get all layers in the registry."""
        for layer in self.layers():
            name = type(layer).__name__
            attrName = name[:1].lower() + name[1:]
            setattr(workspace, attrName, layer)
            layer.connectWorkspace(workspace)

    def __layerKey(self, layerType):
        if isinstance(layerType, type):
            return layerType.__name__
        elif isinstance(layerType, str):
            return layerType
        return None

    def objectToValue(self, layer):
        if isinstance(layer, QgsMapLayer):
            return layer.id()
        return layer

    def valueToObject(self, val):
        if isinstance(val, str):
            return QgsProject.instance().mapLayer(val)
        return val
