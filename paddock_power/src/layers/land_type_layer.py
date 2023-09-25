# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ..utils import PLUGIN_FOLDER
from .features import LandType
from .importable_feature_layer import ImportableFeatureLayer


class LandTypeLayer(ImportableFeatureLayer):

    LAYER_NAME = "Land Types"
    STYLE = "land_type"

    @classmethod
    def getFeatureType(cls):
        return LandType

    def __init__(self, workspaceFile, *dependentLayers):
        super().__init__(workspaceFile,
                         layerName=LandTypeLayer.defaultName(),
                         styleName=LandTypeLayer.defaultStyle())

        self.setReadOnly(False)

    @classmethod
    def icon(cls):
        """The icon to paint to represent this layer."""
        return QIcon(f":/plugins/{PLUGIN_FOLDER}/images/land-type.png")
