# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature, QgsField, QgsFields

from ...models.paddock_power_error import WaterpointBufferPowerError
from .area_feature import AreaFeature


class WaterpointBuffer(AreaFeature):
    BUFFER_DISTANCE, WATERED_AREA = ["Buffer Distance (km)",
                                     "Watered Area (km²)"]


    SCHEMA = AreaFeature.SCHEMA + [
        QgsField(name=BUFFER_DISTANCE, type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=WATERED_AREA, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
    ]

    def bufferDistance(self):
        return self[WaterpointBuffer.BUFFER_DISTANCE]

    def wateredArea(self):
        return self[WaterpointBuffer.WATERED_AREA]

    def recalculate(self, bufferDistance, landSystemLayer = None):
        """Recalculate stats for this Waterpoint Buffer"""
        # TODO
        pass

WaterpointBufferFeature = type('WaterpointBufferFeature', (WaterpointBuffer, QgsFeature), {})

def asWaterpointBuffer(feature):
    """Return a WaterpointBuffer object from a QgsFeature."""
    if not isinstance(feature, QgsFeature):
        raise WaterpointBufferPowerError("asWaterpointBuffer: feature is not a QgsFeature")
    if not isinstance(feature, WaterpointBuffer):
        feature.__class__ = WaterpointBufferFeature
    return feature


def makeWaterpointBuffer():
    """Return a new and empty WaterpointBuffer object."""
    fields = QgsFields()
    for field in WaterpointBuffer.SCHEMA:
        fields.append(field)

    feature = QgsFeature(fields)
    return asWaterpointBuffer(feature)
