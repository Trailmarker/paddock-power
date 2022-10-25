# -*- coding: utf-8 -*-
# from functools import cached_property

from qgis.core import QgsFeatureRequest, QgsGeometry

from ..features.waterpoint_buffer import WaterpointBuffer
from ..features.waterpoint_buffer_type import WaterpointBufferType
from ..features.schemas import WATERPOINT_BUFFER_TYPE
from .feature_layer import FeatureLayer


class WaterpointBufferLayer(FeatureLayer):

    # STYLE = "waterpoint_buffer"
    @classmethod
    def getFeatureType(cls):
        return WaterpointBuffer

    def __init__(self, gpkgFile, layerName):
        """Create or open a Waterpoint layer."""

        super().__init__(gpkgFile, layerName, styleName=None)

    def invalidateNearAndFarBuffers(self):
        del self.getNearAndFarBuffers

    def getNearAndFarBuffers(self):

        nearBufferRequest = QgsFeatureRequest().setFilterExpression(
            f'"{WATERPOINT_BUFFER_TYPE}" = \'{WaterpointBufferType.Near.name}\'')
        nearBuffers = self.getFeatures(nearBufferRequest)
        nearBufferGeom = QgsGeometry.unaryUnion(b.geometry for b in nearBuffers)

        farBufferRequest = QgsFeatureRequest().setFilterExpression(
            f'"{WATERPOINT_BUFFER_TYPE}" = \'{WaterpointBufferType.Far.name}\'')
        farBuffers = self.getFeatures(farBufferRequest)
        farBufferGeom = QgsGeometry.unaryUnion(b.geometry for b in farBuffers)

        # Subtract the near buffer from the far buffer so they do not overlap
        farBufferGeom = farBufferGeom.difference(nearBufferGeom)

        nearBuffer = self.makeFeature()
        nearBuffer.geometry = nearBufferGeom
        nearBuffer.waterpointBufferType = WaterpointBufferType.Near

        farBuffer = self.makeFeature()
        farBuffer.geometry = farBufferGeom
        farBuffer.waterpointBufferType = WaterpointBufferType.Far

        return nearBuffer, farBuffer
