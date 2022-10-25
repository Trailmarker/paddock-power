# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsWkbTypes

from .condition import Condition
from .feature_status import FeatureStatus
from .field import DomainField, IdField, MeasureField, StringField
from .waterpoint_buffer_type import WaterpointBufferType
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
Fid = IdField("id", name=FID)
NAME = "Name"
Name = StringField(propertyName="name", name=NAME)
FeatureSchema = Schema([Fid, Name])

STATUS = "Status"
Status = DomainField(propertyName="status", name=STATUS, domainType=FeatureStatus, defaultValue=FeatureStatus.Undefined)
StatusFeatureSchema = Schema(FeatureSchema + [Status])

LONGITUDE = "Longitude"
Longitude = MeasureField(propertyName="featureLongitude", name=LONGITUDE, defaultValue=float('NaN'))
LATITUDE = "Latitude"
Latitude = MeasureField(propertyName="featureLatitude", name=LATITUDE, defaultValue=float('NaN'))
ELEVATION = "Elevation (m)"
Elevation = MeasureField(propertyName="featureElevation", name=ELEVATION, defaultValue=float('NaN'))
PointFeatureSchema = Schema(StatusFeatureSchema + [Longitude, Latitude, Elevation], wkbType=QgsWkbTypes.Point)

LENGTH = "Length (km)"
Length = MeasureField(propertyName="featureLength", name=LENGTH)
LineFeatureSchema = Schema(StatusFeatureSchema + [Length], wkbType=QgsWkbTypes.LineString)

PipelineSchema = LineFeatureSchema

AREA = "Area (km²)"
Area = MeasureField(propertyName="featureArea", name=AREA)
PERIMETER = "Perimeter (km)"
Perimeter = MeasureField(propertyName="featurePerimeter", name=PERIMETER)
AreaFeatureSchema = Schema(StatusFeatureSchema + [Area, Perimeter], wkbType=QgsWkbTypes.MultiPolygon)

BoundarySchema = AreaFeatureSchema

CAPACITY_PER_AREA = "AE/km²"
CapacityPerArea = MeasureField(propertyName="capacityPerArea", name=CAPACITY_PER_AREA)
CAPACITY = "AE"
EstimatedCapacity = MeasureField(propertyName="estimatedCapacity", name=CAPACITY)
POTENTIAL_CAPACITY = "Potential AE"
PotentialCapacity = MeasureField(propertyName="potentialCapacity", name=POTENTIAL_CAPACITY)

BUILD_ORDER = "Build Order"
FenceSchema = Schema(LineFeatureSchema + [
    IdField(propertyName="buildOrder", name=BUILD_ORDER)
])

MAP_UNIT = "Map Unit"
LANDSCAPE_CLASS = "Landscape Class"
CLASS_DESCRIPTION = "Class Description"
EROSION_RISK = "Erosion Risk"
LandSystemSchema = Schema(FeatureSchema + [Area, Perimeter, CapacityPerArea] + [
    StringField(propertyName="mapUnit", name=MAP_UNIT),
    StringField(propertyName="landscapeClass", name=LANDSCAPE_CLASS),
    StringField(propertyName="classDescription", name=CLASS_DESCRIPTION),
    StringField(propertyName="erosionRisk", name=EROSION_RISK)
], wkbType=QgsWkbTypes.MultiPolygon)

BUILD_FENCE = "Build Fence"
BuildFence = IdField(propertyName="buildFence", name=BUILD_FENCE)
PaddockSchema = Schema(AreaFeatureSchema + [BuildFence, CapacityPerArea, EstimatedCapacity, PotentialCapacity])

WATERPOINT = "Waterpoint"
WATERPOINT_BUFFER_TYPE = "Waterpoint Buffer Type"
WaterpointBufferTypeField = DomainField(
    propertyName="waterpointBufferType",
    name=WATERPOINT_BUFFER_TYPE,
    domainType=WaterpointBufferType)
BUFFER_DISTANCE = "Buffer Distance (m)"
WaterpointBufferSchema = Schema(FeatureSchema + [
    IdField(propertyName="waterpoint", name=WATERPOINT),
    WaterpointBufferTypeField,
    MeasureField(propertyName="bufferDistance", name=BUFFER_DISTANCE)
], wkbType=QgsWkbTypes.MultiPolygon)

WATERPOINT_TYPE = "Waterpoint Type"
REFERENCE = "Reference"
BORE_YIELD = "Bore Yield (L/s)"
BORE_REPORT_URL = "Bore Report URL"
WATERPOINT_START_MONTH = "Waterpoint Start Month"
WATERPOINT_END_MONTH = "Waterpoint End Month"
NEAR_BUFFER = "Near Buffer (m)"
FAR_BUFFER = "Far Buffer (m)"
WaterpointSchema = Schema(PointFeatureSchema + [
    DomainField(propertyName="waterpointType", name=WATERPOINT_TYPE, domainType=WaterpointType, defaultValue=WaterpointType.Bore),
    StringField(propertyName="reference", name=REFERENCE),
    MeasureField(propertyName="boreYield", name=BORE_YIELD),
    StringField(propertyName="boreReportUrl", name=BORE_REPORT_URL),
    StringField(propertyName="waterpointStartMonth", name=WATERPOINT_START_MONTH),
    StringField(propertyName="waterpointEndMonth", name=WATERPOINT_END_MONTH),
    MeasureField(propertyName="nearBuffer", name=NEAR_BUFFER, defaultValue="3000.0"),
    MeasureField(propertyName="farBuffer", name=FAR_BUFFER, defaultValue="5000.0")
])

CONDITION = "Condition"
ConditionField = DomainField(propertyName="condition", name=CONDITION, domainType=Condition, defaultValue=Condition.A)
PADDOCK = "Paddock"
Paddock = IdField(propertyName="paddock", name=PADDOCK)
PADDOCK_NAME = "Paddock Name"
PaddockName = StringField(propertyName="paddockName", name=PADDOCK_NAME)
LAND_SYSTEM = "Land System"
LandSystem = IdField(propertyName="landSystem", name=LAND_SYSTEM)
LAND_SYSTEM_NAME = "Land System Name"
LandSystemName = StringField(propertyName="landSystemName", name=LAND_SYSTEM_NAME)
ConditionRecordSchema = Schema(
    FeatureSchema + [Area, Perimeter, CapacityPerArea, EstimatedCapacity, PotentialCapacity] +
    [ConditionField, Paddock, PaddockName, LandSystem, LandSystemName, WaterpointBufferTypeField],
    wkbType=QgsWkbTypes.MultiPolygon)
