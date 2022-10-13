# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from .paddock import Paddock, asPaddock
from .paddock_power_vector_layer import (PaddockPowerLayerSourceType,
                                         PaddockPowerVectorLayer,
                                         PaddockPowerVectorLayerType)


class PaddockLayer(PaddockPowerVectorLayer):

    STYLE = "paddock"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Paddock layer."""

        super(PaddockLayer, self).__init__(sourceType,
                                           layerName,
                                           QgsWkbTypes.MultiPolygon,
                                           Paddock.SCHEMA,
                                           gpkgFile,
                                           styleName=self.STYLE)
        # Convert all QGIS features to Paddocks
        self.setFeatureAdapter(asPaddock)

    def getLayerType(self):
        """Return the Paddock Power layer type."""
        return PaddockPowerVectorLayerType.Paddock

    def updatePaddock(self, paddockFeature):
        """Update a Paddock feature."""
        self.whileEditing(lambda: self.updateFeature(paddockFeature))

    def updatePaddockName(self, paddockFeature, paddockName):
        """Update a Paddock feature's name."""
        paddockFeature.setPaddockName(paddockName)
        self.updatePaddock(paddockFeature)
 
  