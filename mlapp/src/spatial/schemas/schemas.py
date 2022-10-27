# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from .condition_type import ConditionType
from .feature_status import FeatureStatus
from .field import DomainField, IdField, MeasureField, StringField
from .watered_type import WateredType
from .waterpoint_buffer_type import WaterpointBufferType
from .waterpoint_type import WaterpointType


class ReadOnlySchema(list):
    def __init__(self, fieldList, wkbType=None):
        super().__init__(fieldList)
        self._wkbType = wkbType

    def addSchema(self):
        def addSchemaToFeatureClass(cls):
            for field in self:
                if field._propertyName is not None:
                    field.addReadOnlyFieldProperty(cls)
                setattr(cls, "getSchema", classmethod(lambda _: self))
            if self._wkbType is not None:
                setattr(cls, "getWkbType", classmethod(lambda _: self._wkbType))
            return cls
        return addSchemaToFeatureClass


class Schema(ReadOnlySchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def addSchema(self):
        def addSchemaToFeatureClass(cls):
            for field in self:
                if field._propertyName is not None:
                    field.addFieldProperty(cls)
                setattr(cls, "getSchema", classmethod(lambda _: self))
            if self._wkbType is not None:
                setattr(cls, "getWkbType", classmethod(lambda _: self._wkbType))
            return cls
        return addSchemaToFeatureClass


AREA = "Area (km²)"
BORE_REPORT_URL = "Bore Report URL"
BORE_YIELD = "Bore Yield (L/s)"
BUFFER_DISTANCE = "Buffer Distance (m)"
BUILD_FENCE = "Build Fence"
BUILD_ORDER = "Build Order"
CAPACITY_PER_AREA = "AE/km²"
CLASS_DESCRIPTION = "Class Description"
CONDITION_TYPE = "Condition"
ELEVATION = "Elevation (m)"
EROSION_RISK = "Erosion Risk"
ESTIMATED_CAPACITY = "AE"
FAR_BUFFER = "Far Buffer (m)"
FID = "fid"
LAND_SYSTEM = "Land System"
LAND_SYSTEM_NAME = "Land System Name"
LANDSCAPE_CLASS = "Landscape Class"
LATITUDE = "Latitude"
LENGTH = "Length (km)"
LONGITUDE = "Longitude"
MAP_UNIT = "Map Unit"
NAME = "Name"
NEAR_BUFFER = "Near Buffer (m)"
PADDOCK = "Paddock"
PADDOCK_NAME = "Paddock Name"
PERIMETER = "Perimeter (km)"
POTENTIAL_CAPACITY = "Potential AE"
REFERENCE = "Reference"
STATUS = "Status"
WATERED_TYPE = "Watered"
WATERPOINT = "Waterpoint"
WATERPOINT_BUFFER_TYPE = "Waterpoint Buffer Type"
WATERPOINT_END_MONTH = "Waterpoint End Month"
WATERPOINT_START_MONTH = "Waterpoint Start Month"
WATERPOINT_TYPE = "Waterpoint Type"

Area = MeasureField(propertyName="featureArea", name=AREA)
BoreReportUrl = StringField(propertyName="boreReportUrl", name=BORE_REPORT_URL)
BoreYield = MeasureField(propertyName="boreYield", name=BORE_YIELD)
BufferDistance = MeasureField(propertyName="bufferDistance", name=BUFFER_DISTANCE)
BuildFence = IdField(propertyName="buildFence", name=BUILD_FENCE)
BuildOrder = IdField(propertyName="buildOrder", name=BUILD_ORDER)
CapacityPerArea = MeasureField(propertyName="capacityPerArea", name=CAPACITY_PER_AREA)
ClassDescription = StringField(propertyName="classDescription", name=CLASS_DESCRIPTION)
ConditionTypeField = DomainField(
    propertyName="condition",
    name=CONDITION_TYPE,
    domainType=ConditionType,
    defaultValue=ConditionType.A)
Elevation = MeasureField(propertyName="featureElevation", name=ELEVATION, defaultValue=float('NaN'))
ErosionRisk = StringField(propertyName="erosionRisk", name=EROSION_RISK)
EstimatedCapacity = MeasureField(propertyName="estimatedCapacity", name=ESTIMATED_CAPACITY)
FarBufferDistance = MeasureField(propertyName="farBuffer", name=FAR_BUFFER, defaultValue="5000.0")
Fid = IdField("id", name=FID)
LandscapeClass = StringField(propertyName="landscapeClass", name=LANDSCAPE_CLASS)
LandSystem = IdField(propertyName="landSystem", name=LAND_SYSTEM)
LandSystemName = StringField(propertyName="landSystemName", name=LAND_SYSTEM_NAME)
Latitude = MeasureField(propertyName="featureLatitude", name=LATITUDE, defaultValue=float('NaN'))
Length = MeasureField(propertyName="featureLength", name=LENGTH)
Longitude = MeasureField(propertyName="featureLongitude", name=LONGITUDE, defaultValue=float('NaN'))
MapUnit = StringField(propertyName="mapUnit", name=MAP_UNIT)
Name = StringField(propertyName="name", name=NAME)
NearBufferDistance = MeasureField(propertyName="nearBuffer", name=NEAR_BUFFER, defaultValue="3000.0")
Paddock = IdField(propertyName="paddock", name=PADDOCK)
PaddockName = StringField(propertyName="paddockName", name=PADDOCK_NAME)
Perimeter = MeasureField(propertyName="featurePerimeter", name=PERIMETER)
PotentialCapacity = MeasureField(propertyName="potentialCapacity", name=POTENTIAL_CAPACITY)
Reference = StringField(propertyName="reference", name=REFERENCE)
Status = DomainField(propertyName="status", name=STATUS, domainType=FeatureStatus, defaultValue=FeatureStatus.Undefined)
WateredTypeField = DomainField(propertyName="wateredType", name=WATERED_TYPE, domainType=WateredType, defaultValue=WateredType.Unwatered)
Waterpoint = IdField(propertyName="waterpoint", name=WATERPOINT)
WaterpointBufferTypeField = DomainField(
    propertyName="waterpointBufferType",
    name=WATERPOINT_BUFFER_TYPE,
    domainType=WaterpointBufferType)
WaterpointEndMonth = StringField(propertyName="waterpointEndMonth", name=WATERPOINT_END_MONTH)
WaterpointStartMonth = StringField(propertyName="waterpointStartMonth", name=WATERPOINT_START_MONTH)
WaterpointTypeField = DomainField(
    propertyName="waterpointType",
    name=WATERPOINT_TYPE,
    domainType=WaterpointType,
    defaultValue=WaterpointType.Bore)

AreaFeatureSchema = Schema([Fid, Name, Status, Area, Perimeter], wkbType=QgsWkbTypes.MultiPolygon)
BoundarySchema = ReadOnlySchema([Fid, Status], wkbType=QgsWkbTypes.MultiPolygon)
ConditionSchema = ReadOnlySchema([#Fid,
                                  #Status,
                                  Area,
                                  CapacityPerArea,
                                  EstimatedCapacity,
                                  PotentialCapacity,
                                  ConditionTypeField,
                                  Paddock,
                                  PaddockName,
                                  LandSystem,
                                  LandSystemName,
                                  WateredTypeField],
                                 wkbType=QgsWkbTypes.MultiPolygon)
FeatureSchema = ReadOnlySchema([Fid])
FenceSchema = Schema([Fid, Name, Status, Length, BuildOrder], wkbType=QgsWkbTypes.LineString)
LandSystemSchema = Schema([Fid, Name, Area, Perimeter, CapacityPerArea, MapUnit, LandscapeClass,
                          ClassDescription, ErosionRisk], wkbType=QgsWkbTypes.MultiPolygon)
LineFeatureSchema = Schema([Fid, Name, Status, Length], wkbType=QgsWkbTypes.LineString)
PaddockSchema = Schema([Fid, Name, Status, Area, Perimeter, BuildFence, CapacityPerArea,
                       EstimatedCapacity, PotentialCapacity], wkbType=QgsWkbTypes.MultiPolygon)
PersistedFeatureSchema = Schema([Fid])
PipelineSchema = LineFeatureSchema
PointFeatureSchema = Schema([Fid, Name, Status, Longitude, Latitude, Elevation], wkbType=QgsWkbTypes.Point)
StatusFeatureSchema = Schema([Fid, Name, Status])
WaterpointBufferSchema = ReadOnlySchema([Status, Waterpoint, WaterpointBufferTypeField, BufferDistance],
    wkbType=QgsWkbTypes.MultiPolygon)
WateredAreaSchema = ReadOnlySchema([Fid, WateredTypeField, Status], wkbType=QgsWkbTypes.MultiPolygon)
WaterpointSchema = Schema([Fid,
                           Name,
                           Status,
                           Longitude,
                           Latitude,
                           Elevation,
                           WaterpointTypeField,
                           NearBufferDistance,
                           FarBufferDistance],
                          wkbType=QgsWkbTypes.Point)
