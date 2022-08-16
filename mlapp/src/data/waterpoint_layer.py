# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsWkbTypes

from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerVectorLayerSourceType, PaddockPowerVectorLayerType


class WaterpointLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="fid", type=QVariant.LongLong, typeName="Integer64",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Type", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Name", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Reference", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Bore Yield (l/sec)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Bore Report", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Status", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Date Commisioned", type=QVariant.Date,
                 typeName="Date", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Date Decommisioned", type=QVariant.Date,
                 typeName="Date", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Start Month", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint End Month", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Longitude", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Latitude", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Elevation", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Date Edited", type=QVariant.Date, typeName="Date",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    STYLE = "waterpoint"
    TYPE = PaddockPowerVectorLayerType.Waterpoint

    def __init__(self, sourceType=PaddockPowerVectorLayerSourceType.Memory, layerName=None, gpkgUrl=None):
        """Create or open a Waterpoint layer."""

        super(WaterpointLayer, self).__init__(sourceType,
                                              layerName,
                                              QgsWkbTypes.Point,
                                              self.SCHEMA,
                                              gpkgUrl,
                                              styleName=self.STYLE)
