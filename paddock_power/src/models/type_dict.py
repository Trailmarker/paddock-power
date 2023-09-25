# -*- coding: utf-8 -*-
from ..utils import PLUGIN_NAME
from .glitch import Glitch


class TypeDict(dict):
    def __init__(self):
        f"""A dictionary with types as keys and some convenience functions."""
        super().__init__()

    def addObject(self, layerType, layer):
        """Add a layer to the registry."""

        if not isinstance(layerType, type):
            raise Glitch(f"Invalid TypeDict key: must be a type")

        self[self._layerKey(layerType)] = self.objectToValue(layer)

    def getObject(self, layerType):
        val = self.valueToObject(self.get(self._layerKey(layerType), None))
        return val

    def allObjects(self):
        """Get all layers in the registry."""
        return list(map(self.valueToObject, self.values()))

    def _layerKey(self, layerType):
        if isinstance(layerType, type):
            return layerType.__name__
        elif isinstance(layerType, str):
            return layerType
        return None

    def objectToValue(self, obj):
        return obj

    def valueToObject(self, val):
        return val
