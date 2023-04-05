# -*- coding: utf-8 -*-
from qgis.core import QgsMapLayer, QgsProject

from ..layers import BasePaddockLayer, LandTypeLayer, WaterpointLayer
from ..layers.interfaces import IFeatureLayer, IImportableFeatureLayer, ILayer
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

    def hasFeatures(self, layerType):
        """Check if the layer for the given layer type has features."""
        layer = self.layer(layerType)
        return layer and layer.hasFeatures

    @property
    def hasBasePaddocks(self):
        """Check if the base paddock layer has features."""
        return self.hasFeatures(BasePaddockLayer)

    @property
    def isAnalytic(self):
        """Check if the workspace is analytic."""
        return self.hasBasePaddocks and self.hasFeatures(LandTypeLayer) and self.hasFeatures(WaterpointLayer)

    def layers(self):
        """Get all layers in the registry."""
        return list(map(self.valueToObject, self.values()))

    def featureLayers(self):
        """Get all layers in the registry."""
        return [l for l in self.layers() if isinstance(l, IFeatureLayer)]

    def importableFeatureLayers(self):
        """Get all importable layers in the registry."""
        return [l for l in self.layers() if isinstance(l, IImportableFeatureLayer)]

    def unloadLayer(self, layerType):
        """Unload the layer of the given type."""
        layer = self.valueToObject(self.pop(self.__layerKey(layerType), None))
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

    def objectToValue(self, layer):
        if isinstance(layer, QgsMapLayer):
            return layer.id()
        return layer

    def valueToObject(self, val):
        if isinstance(val, str):
            return QgsProject.instance().mapLayer(val)
        return val
