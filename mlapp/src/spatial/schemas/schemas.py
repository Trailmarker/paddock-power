# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from .condition_type import ConditionType
from .feature_status import FeatureStatus
from .field import DomainField, IdField, MeasureField, StringField
from .watered_type import WateredType
from .grazing_radius_type import GrazingRadiusType
from .waterpoint_type import WaterpointType


class ReadOnlySchema(list):
    def __init__(self, fieldList, wkbType=None):
        super().__init__(fieldList)
        self._wkbType = wkbType

    def addSchema(self):
        def _addSchema(cls):
            for field in self:
                if field._propertyName is not None:
                    field.addReadOnlyFieldProperty(cls)
                setattr(cls, "getSchema", classmethod(lambda _: self))
            if self._wkbType is not None:
                setattr(cls, "getWkbType", classmethod(lambda _: self._wkbType))
            return cls
        return _addSchema


class Schema(ReadOnlySchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def addSchema(self):
        def _addSchema(cls):
            for field in self:
                if field._propertyName is not None:
                    field.addFieldProperty(cls)
                setattr(cls, "getSchema", classmethod(lambda _: self))
            if self._wkbType is not None:
                setattr(cls, "getWkbType", classmethod(lambda _: self._wkbType))
            return cls
        return _addSchema


AREA = "Area (km²)"
BORE_REPORT_URL = "Bore Report URL"
BORE_YIELD = "Bore Yield (L/s)"
BUILD_FENCE = "Build Fence"
BUILD_ORDER = "Build Order"
CLASS_DESCRIPTION = "Class Description"
CONDITION_DISCOUNT = "Condition Discount"
CONDITION_TYPE = "Condition"
ELEVATION = "Elevation (m)"
EROSION_RISK = "Erosion Risk"
ESTIMATED_CAPACITY = "AE"
ESTIMATED_CAPACITY_PER_AREA = "AE/km²"
FAR_GRAZING_RADIUS = "Far Grazing Radius (m)"
FID = "fid"
GRAZING_RADIUS = "Grazing Radius (m)"
GRAZING_RADIUS_TYPE = "Grazing Radius Type"
LAND_SYSTEM = "Land System"
LAND_SYSTEM_NAME = "Land System Name"
LANDSCAPE_CLASS = "Landscape Class"
LATITUDE = "Latitude"
LENGTH = "Length (km)"
LONGITUDE = "Longitude"
MAP_UNIT = "Map Unit"
NAME = "Name"
NEAR_GRAZING_RADIUS = "Near Grazing Radius (m)"
PADDOCK = "Paddock"
PADDOCK_NAME = "Paddock Name"
PADDOCK_STATUS = "Paddock Status"
PERIMETER = "Perimeter (km)"
POTENTIAL_CAPACITY = "Potential AE"
POTENTIAL_CAPACITY_PER_AREA = "Potential AE/km²"
RECALCULATE_COMPLETE = "Complete"
RECALCULATE_CURRENT = "Current"
REFERENCE = "Reference"
STATUS = "Status"
WATERED_AREA_STATUS = "Watered Area Status"
WATERED_DISCOUNT = "Watered Discount"
WATERED_TYPE = "Watered"
WATERPOINT = "Waterpoint"
WATERPOINT_END_MONTH = "Waterpoint End Month"
WATERPOINT_START_MONTH = "Waterpoint Start Month"
WATERPOINT_TYPE = "Waterpoint Type"


Area = MeasureField(propertyName="featureArea", name=AREA)
BoreReportUrl = StringField(propertyName="boreReportUrl", name=BORE_REPORT_URL)
BoreYield = MeasureField(propertyName="boreYield", name=BORE_YIELD)
GrazingRadius = MeasureField(propertyName="grazingRadius", name=GRAZING_RADIUS)
BuildFence = IdField(propertyName="buildFence", name=BUILD_FENCE)
BuildOrder = IdField(propertyName="buildOrder", name=BUILD_ORDER)
ClassDescription = StringField(propertyName="classDescription", name=CLASS_DESCRIPTION)
ConditionTypeField = DomainField(
    propertyName="conditionType",
    name=CONDITION_TYPE,
    domainType=ConditionType,
    defaultValue=ConditionType.A)
Elevation = MeasureField(propertyName="featureElevation", name=ELEVATION, defaultValue=float('NaN'))
ErosionRisk = StringField(propertyName="erosionRisk", name=EROSION_RISK)
EstimatedCapacity = MeasureField(propertyName="estimatedCapacity", name=ESTIMATED_CAPACITY)
EstimatedCapacityPerArea = MeasureField(propertyName="estimatedCapacityPerArea", name=ESTIMATED_CAPACITY_PER_AREA)
FarGrazingRadius = MeasureField(propertyName="farGrazingRadius", name=FAR_GRAZING_RADIUS, defaultValue="5000.0")
Fid = IdField("id", name=FID)
LandscapeClass = StringField(propertyName="landscapeClass", name=LANDSCAPE_CLASS)
LandSystem = IdField(propertyName="landSystem", name=LAND_SYSTEM)
LandSystemName = StringField(propertyName="landSystemName", name=LAND_SYSTEM_NAME)
Latitude = MeasureField(propertyName="featureLatitude", name=LATITUDE, defaultValue=float('NaN'))
Length = MeasureField(propertyName="featureLength", name=LENGTH)
Longitude = MeasureField(propertyName="featureLongitude", name=LONGITUDE, defaultValue=float('NaN'))
MapUnit = StringField(propertyName="mapUnit", name=MAP_UNIT)
Name = StringField(propertyName="name", name=NAME)
NearGrazingRadius = MeasureField(propertyName="nearGrazingRadius", name=NEAR_GRAZING_RADIUS, defaultValue="3000.0")
Paddock = IdField(propertyName="paddock", name=PADDOCK)
PaddockName = StringField(propertyName="paddockName", name=PADDOCK_NAME)
PaddockStatus = DomainField(
    propertyName="paddockStatus",
    name=PADDOCK_STATUS,
    domainType=FeatureStatus,
    defaultValue=FeatureStatus.Undefined)
Perimeter = MeasureField(propertyName="featurePerimeter", name=PERIMETER)
PotentialCapacity = MeasureField(propertyName="potentialCapacity", name=POTENTIAL_CAPACITY)
PotentialCapacityPerArea = MeasureField(propertyName="potentialCapacityPerArea", name=POTENTIAL_CAPACITY_PER_AREA)
RecalculateCurrent = IdField(propertyName="recalculateCurrent", name=RECALCULATE_CURRENT)
RecalculateComplete = IdField(propertyName="recalculateComplete", name=RECALCULATE_COMPLETE)
Reference = StringField(propertyName="reference", name=REFERENCE)
Status = DomainField(propertyName="status", name=STATUS, domainType=FeatureStatus, defaultValue=FeatureStatus.Undefined)
WateredTypeField = DomainField(
    propertyName="wateredType",
    name=WATERED_TYPE,
    domainType=WateredType,
    defaultValue=WateredType.Unwatered)
Waterpoint = IdField(propertyName="waterpoint", name=WATERPOINT)
GrazingRadiusTypeField = DomainField(
    propertyName="grazingRadiusType",
    name=GRAZING_RADIUS_TYPE,
    domainType=GrazingRadiusType)
WaterpointEndMonth = StringField(propertyName="waterpointEndMonth", name=WATERPOINT_END_MONTH)
WaterpointStartMonth = StringField(propertyName="waterpointStartMonth", name=WATERPOINT_START_MONTH)
WaterpointTypeField = DomainField(
    propertyName="waterpointType",
    name=WATERPOINT_TYPE,
    domainType=WaterpointType,
    defaultValue=WaterpointType.Bore)

AreaFeatureSchema = Schema([Fid, Name, Status, Area, Perimeter], wkbType=QgsWkbTypes.MultiPolygon)
BoundarySchema = Schema([Fid, Status], wkbType=QgsWkbTypes.MultiPolygon)
ConditionSchema = Schema([Fid,
                          # Status,
                          Area,
                          EstimatedCapacityPerArea,
                          PotentialCapacityPerArea,
                          EstimatedCapacity,
                          PotentialCapacity,
                          ConditionTypeField,
                          Paddock,
                          PaddockName,
                          LandSystem,
                          LandSystemName,
                          WateredTypeField],
                         wkbType=QgsWkbTypes.MultiPolygon)
FeatureSchema = Schema([Fid])
FenceSchema = Schema([Fid, Name, Status, Length, BuildOrder], wkbType=QgsWkbTypes.LineString)
LandSystemSchema = Schema([Fid, Name, Area, Perimeter, EstimatedCapacityPerArea, MapUnit, LandscapeClass,
                          ClassDescription, ErosionRisk], wkbType=QgsWkbTypes.MultiPolygon)
LineFeatureSchema = Schema([Fid, Name, Status, Length], wkbType=QgsWkbTypes.LineString)
PaddockSchema = Schema([Fid,
                        Name,
                        Status,
                        Area,
                        Perimeter,
                        BuildFence,
                        EstimatedCapacityPerArea,
                        EstimatedCapacity,
                        PotentialCapacityPerArea,
                        PotentialCapacity,
                        RecalculateCurrent,
                        RecalculateComplete],
                       wkbType=QgsWkbTypes.MultiPolygon)
PersistedFeatureSchema = Schema([Fid], wkbType=QgsWkbTypes.MultiPolygon)
PipelineSchema = LineFeatureSchema
PointFeatureSchema = Schema([Fid, Name, Status, Longitude, Latitude, Elevation], wkbType=QgsWkbTypes.Point)
StatusFeatureSchema = Schema([Fid, Name, Status])
WaterpointBufferSchema = Schema(
    [Fid, Status, Paddock, Waterpoint, GrazingRadiusTypeField, GrazingRadius, PaddockStatus],
    wkbType=QgsWkbTypes.MultiPolygon)
WateredAreaSchema = Schema([Fid, WateredTypeField, Status, Paddock, PaddockStatus], wkbType=QgsWkbTypes.MultiPolygon)
WaterpointSchema = Schema([Fid,
                           Name,
                           Status,
                           Longitude,
                           Latitude,
                           Elevation,
                           WaterpointTypeField,
                           NearGrazingRadius,
                           FarGrazingRadius],
                          wkbType=QgsWkbTypes.Point)
