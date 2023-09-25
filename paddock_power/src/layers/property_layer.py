# -*- coding: utf-8 -*-

from ..utils import PLUGIN_NAME
from .features import Property
from .derived_property_layer import DerivedPropertyLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class PropertyLayer(PersistedDerivedFeatureLayer):

    LAYER_NAME = "Property"
    STYLE = "property"

    @classmethod
    def getFeatureType(cls):
        return Property

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        f"""Create a new {PLUGIN_NAME} Property layer."""

        super().__init__(workspaceFile,
                         PropertyLayer.defaultName(),
                         PropertyLayer.defaultStyle(),
                         DerivedPropertyLayer,
                         dependentLayers)
