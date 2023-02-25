# -*- coding: utf-8 -*-

from ..utils import PLUGIN_NAME
from .features import Boundary
from .derived_boundary_layer import DerivedBoundaryLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class BoundaryLayer(PersistedDerivedFeatureLayer):

    LAYER_NAME = "Boundary"
    STYLE = "boundary"

    @classmethod
    def getFeatureType(cls):
        return Boundary

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        f"""Create a new {PLUGIN_NAME} Paddock Land Types layer."""

        super().__init__(workspaceFile,
                         BoundaryLayer.defaultName(),
                         BoundaryLayer.defaultStyle(),
                         DerivedBoundaryLayer,
                         dependentLayers)
