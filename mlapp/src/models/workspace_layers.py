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
        
        val = layer
        if isinstance(layer, QgsMapLayer):
            val = layer.id()
                        
        self[layerType.__name__] = val

    def getLayer(self, layerType):
        """Get the layer for the given layer type."""

        # We support the case where the layerType is a string, because 
        # it's useful when citing types causes circular imports.

        val = None
        if isinstance(layerType, type):
            val = self[layerType.__name__]
        elif isinstance(layerType, str):
            val = self[layerType]
        else:
            raise Glitch(f"Invalid WorkspaceLayers key: must be a type or the string name of a type")

        if isinstance(val, ConditionTable):
            return val
        else:
            return QgsProject.instance().mapLayer(val)
        
    def unloadLayer(self, layerType):
        """Unload the layer of the given type."""
        layer = self.pop(layerType.__name__, None)
        if layer:
            QgsProject.instance().removeMapLayer(layer.id())
            

