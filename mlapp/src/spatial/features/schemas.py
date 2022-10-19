# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsWkbTypes

from .condition import Condition
from .feature_status import FeatureStatus
from .field import Field
from .waterpoint_type import WaterpointType


class Schema(list):
    def __init__(self, fieldList, wkbType=None):
        super().__init__(fieldList)
        self._wkbType = wkbType

    def addSchema(self):
        def addSchemaToFeature(cls):
            for field in self:
                if field._propertyName is not None:
                    field.addFieldProperty(cls)
                setattr(cls, "getSchema", classmethod(lambda _: self))
            if self._wkbType is not None:
                setattr(cls, "getWkbType", classmethod(lambda _: self._wkbType))
            return cls
        return addSchemaToFeature


FID = "fid"
STATUS = "Status"
NAME = "Name"

FeatureSchema = Schema([
    Field(name=FID, type=QVariant.LongLong, typeName="Integer64",
          len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="name", name=NAME, type=QVariant.String, typeName="String",
          len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="status", name=STATUS, type=QVariant.String, typeName="String",
          len=0, prec=0, comment="", subType=QVariant.Invalid,
          domainType=FeatureStatus, defaultValue=FeatureStatus.Undefined)
])

LONGITUDE = "Longitude"
LATITUDE = "Latitude"
ELEVATION = "Elevation (m)"

PointFeatureSchema = Schema(FeatureSchema + [
    Field(propertyName="featureLongitude", name=LONGITUDE, type=QVariant.Double,
          typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="featureLatitude", name=LATITUDE, type=QVariant.Double,
          typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="featureElevation", name=ELEVATION, type=QVariant.Double,
          typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid)
], wkbType=QgsWkbTypes.Point)

LENGTH = "Length (km)"

LineFeatureSchema = Schema(FeatureSchema + [
    Field(propertyName="featureLength", name=LENGTH, type=QVariant.Double, typeName="Real",
          len=0, prec=0, comment="", subType=QVariant.Invalid)
], wkbType=QgsWkbTypes.LineString)

AREA = "Area (km²)"
PERIMETER = "Perimeter (km)"

AreaFeatureSchema = Schema(FeatureSchema + [
    Field(propertyName="featureArea", name=AREA, type=QVariant.Double,
          typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="featurePerimeter", name=PERIMETER, type=QVariant.Double,
          typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid)
], wkbType=QgsWkbTypes.MultiPolygon)

BoundarySchema = AreaFeatureSchema

CAPACITY = "AE/km²"

CapacityFeatureSchema = Schema(AreaFeatureSchema + [
    Field(propertyName="featureCapacity", name="AE/km²", type=QVariant.Double, typeName="Real",
          len=0, prec=0, comment="", subType=QVariant.Invalid)
])

CONDITION = "Condition"
PADDOCK_NAME = "Paddock Name"
LAND_TYPE_NAME = "Land Type Name"
WATERPOINT_BUFFER = "Waterpoint Buffer"
WATERPOINT_BUFFER_DISTANCE = "Waterpoint Buffer Distance"

ConditionRecordSchema = Schema(CapacityFeatureSchema + [
    Field(propertyName="condition", name=CONDITION, type=QVariant.String,
          typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid,
          domainType=Condition, defaultValue=Condition.A),
    Field(propertyName="paddockName", name=PADDOCK_NAME, type=QVariant.String,
          typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="landTypeName", name=LAND_TYPE_NAME, type=QVariant.String,
          typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="waterpointBUffer", name=WATERPOINT_BUFFER, type=QVariant.LongLong,
          typeName="Integer64", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="waterpointBufferDistance", name=WATERPOINT_BUFFER_DISTANCE, type=QVariant.Double,
          typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid)
])

BUILD_ORDER = "Build Order"

FenceSchema = Schema(LineFeatureSchema + [
    Field(propertyName="buildOrder", name=BUILD_ORDER, type=QVariant.LongLong,
          typeName="Integer64", len=0, prec=0, comment="", subType=QVariant.Invalid)
])

MAP_UNIT = "Map Unit"
LANDSCAPE_CLASS = "Landscape Class"
CLASS_DESCRIPTION = "Class Description"
EROSION_RISK = "Erosion Risk"

LandSystemSchema = Schema(CapacityFeatureSchema + [
    Field(propertyName="mapUnit", name="Map Unit", type=QVariant.String,
          typeName="String", len=10, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="landscapeClass", name="Landscape Class", type=QVariant.String,
          typeName="String", len=50, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="classDescription", name="Class Description", type=QVariant.String,
          typeName="String", len=254, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="erosionRisk", name="Erosion Risk", type=QVariant.String,
          typeName="String", len=100, prec=0, comment="", subType=QVariant.Invalid)
])

BUILD_FENCE = "Build Fence"

PaddockSchema = Schema(CapacityFeatureSchema + [
    Field(propertyName="buildFence", name=BUILD_FENCE, type=QVariant.LongLong,
          typeName="Integer64", len=0, prec=0, comment="", subType=QVariant.Invalid),
])

PipelineSchema = LineFeatureSchema

BUFFER_DISTANCE = "Buffer Distance (km)"
WATERED_AREA = "Watered Area (km²)"

WaterpointBufferSchema = Schema(AreaFeatureSchema + [
    Field(propertyName="bufferDistance", name=BUFFER_DISTANCE, type=QVariant.Double, typeName="Real",
          len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="wateredArea", name=WATERED_AREA, type=QVariant.Double,
          typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
])

WATERPOINT_TYPE = "Waterpoint Type"
REFERENCE = "Reference"
BORE_YIELD = "Bore Yield (L/s)"
BORE_REPORT_URL = "Bore Report URL"
WATERPOINT_START_MONTH = "Waterpoint Start Month"
WATERPOINT_END_MONTH = "Waterpoint End Month"

WaterpointSchema = Schema(PointFeatureSchema + [
    Field(propertyName="waterpointType", name=WATERPOINT_TYPE, type=QVariant.String, typeName="String",
          len=0, prec=0, comment="", subType=QVariant.Invalid,
          domainType=WaterpointType),
    Field(propertyName="reference", name=REFERENCE, type=QVariant.String,
          typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="boreYield", name=BORE_YIELD, type=QVariant.Double,
          typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="boreReportUrl", name=BORE_REPORT_URL, type=QVariant.String,
          typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="waterpointStartMonth", name=WATERPOINT_START_MONTH, type=QVariant.String,
          typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
    Field(propertyName="waterpointEndMonth", name=WATERPOINT_END_MONTH, type=QVariant.String,
          typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid)
])
