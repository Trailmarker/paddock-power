# -*- coding: utf-8 -*-
from qgis.core import QgsMapLayer, QgsProject

from ..spatial.layers.condition_table import ConditionTable
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.feature_layer import FeatureLayer
from ..utils import PLUGIN_NAME
from .glitch import Glitch


class WorkspaceLayers(dict):
    def __init__(self, *layers):
        f"""Create a type registry for {PLUGIN_NAME}'s Layer like objects."""
        super().__init__()

        for layer in layers:
            self.addLayer(type(layer), layer)

    def addLayer(self, layerType, layer):
        """Add a layer to the registry."""

        if not isinstance(layerType, type):
            raise Glitch(f"Invalid WorkspaceLayers key: must be a type")

        if not any(map(lambda cls: isinstance(layer, cls), [FeatureLayer, ElevationLayer, ConditionTable])):
            raise Glitch(f"Invalid WorkspaceLayers value: must be a ConditionTable, ElevationLayer or FeatureLayer")

        self[self.__layerKey(layerType)] = self.__setValue(layer)

    def layer(self, layerType):
        """Get the layer for the given layer type."""

        # We support the case where the layerType is a string, because
        # it's useful when citing types causes circular imports.
        val = self.__getValue(self.get(self.__layerKey(layerType), None))
        return val

    def layers(self):
        """Get all layers in the registry."""
        return list(map(self.__getValue, self.values()))

    def featureLayers(self):
        """Get all layers in the registry."""
        return [l for l in self.layers() if isinstance(l, FeatureLayer)]

    def unloadLayer(self, layerType):
        """Unload the layer of the given type."""
        layer = self.__getValue(self.pop(self.__layerKey(layerType), None))
        if isinstance(layer, QgsMapLayer):
            QgsProject.instance().removeMapLayer(layer.id())

    def unloadByName(self, name):
        """Unload all layers in the registry."""
        for layerType in list(self.keys()):
            self.unloadLayer(layerType)

    def __layerKey(self, layerType):
        if isinstance(layerType, type):
            return layerType.__name__
        elif isinstance(layerType, str):
            return layerType
        return None

    def __setValue(self, layer):
        if isinstance(layer, QgsMapLayer):
            return layer.id()
        return layer

    def __getValue(self, val):
        if isinstance(val, str):
            return QgsProject.instance().mapLayer(val)
        return val
