# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from .glitch import Glitch
from ..spatial.layers.condition_table import ConditionTable
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.feature_layer import FeatureLayer

class WorkspaceLayers(dict):
    def __init__(self, *args, **kwargs):
        """Create FeatureLayers registry."""

        self.update(*args, **kwargs)

    def __getitem__(self, __key) -> object:
        """Get the instance for the given FeatureLayer."""
        if not isinstance(__key, type):
            raise Glitch(f"Invalid WorkspaceLayers key: must be a type")
        
        val = super().__getitem__(__key)
        if isinstance(val, ConditionTable):
            return val
        return QgsProject.instance().mapLayer(val) if val else None        

    def __setitem__(self, __key, __value):
        if not isinstance(__key, type):
            raise Glitch(f"Invalid WorkspaceLayers key: must be a type")
        
        if not any(map(lambda cls: isinstance(__value, cls), [FeatureLayer, ElevationLayer, ConditionTable])):
            raise Glitch(f"Invalid WorkspaceLayers value: must be a ConditionTable, ElevationLayer or FeatureLayer")
        
        if isinstance(__value, FeatureLayer):
            super().__setitem__(__key, __value.id())
        if isinstance(__value, ConditionTable):
            super().__setitem__(__key, __value)
        
    def __repr__(self):
        """Return a string representation of the FieldMap."""
        return f"{type(self).__name__}({super().__repr__()})"

    def update(self, *args, **kwargs):
        """Update the FieldMap."""
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
            