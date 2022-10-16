# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsField

from ...calculator import Calculator
from .feature import Feature


class Waterpoint(Feature):
    WATERPOINT_TYPE = "Waterpoint Type"
    REFERENCE = "Reference"
    BORE_YIELD = "Bore Yield (L/s)"
    BORE_REPORT_URL = "Bore Report URL"
    WATERPOINT_START_MONTH = "Waterpoint Start Month"
    WATERPOINT_END_MONTH = "Waterpoint End Month"
    LONGITUDE = "Longitude"
    LATITUDE = "Latitude"
    ELEVATION = "Elevation (m)"

    SCHEMA = Feature.SCHEMA + [
        QgsField(name=WATERPOINT_TYPE, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=REFERENCE, type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=BORE_YIELD, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=BORE_REPORT_URL, type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=WATERPOINT_START_MONTH, type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=WATERPOINT_END_MONTH, type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=LONGITUDE, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=LATITUDE, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=ELEVATION, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def featureLongitude(self):
        return self[Waterpoint.LONGITUDE]

    def featureLatitude(self):
        return self[Waterpoint.LATITUDE]

    def featureElevation(self):
        return self[Waterpoint.ELEVATION]

    def recalculate(self, elevationLayer=None):
        """Recalculate the area and perimeter of the AreaFeature."""
        elevation = round(Calculator.calculateElevationAtPoint(
            self.geometry(), elevationLayer), 2)

        # TODO Latitude and Longitude
        self.feature.setAttribute(Waterpoint.ELEVATION, elevation)
