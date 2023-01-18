# -*- coding: utf-8 -*-
from .names import *

from .condition_type import ConditionType
from .feature_status import FeatureStatus
from .field import DomainField, IdField, MeasureField, StringField
from .timeframe import Timeframe
from .watered_type import WateredType
from .grazing_radius_type import GrazingRadiusType
from .waterpoint_type import WaterpointType


Area = MeasureField(propertyName="featureArea", name=AREA, dps=2)
BoreReportUrl = StringField(propertyName="boreReportUrl", name=BORE_REPORT_URL)
BoreYield = MeasureField(propertyName="boreYield", name=BORE_YIELD)
GrazingRadius = MeasureField(propertyName="grazingRadius", name=GRAZING_RADIUS, dps=0)
BuildFence = IdField(propertyName="buildFence", name=BUILD_FENCE)
BuildOrder = IdField(propertyName="buildOrder", name=BUILD_ORDER)
ClassDescription = StringField(propertyName="classDescription", name=CLASS_DESCRIPTION)
ConditionTypeField = DomainField(
    propertyName="conditionType",
    name=CONDITION_TYPE,
    domainType=ConditionType,
    defaultValue=ConditionType.A)
Elevation = MeasureField(propertyName="featureElevation", name=ELEVATION, defaultValue=float('NaN'), dps=1)
ErosionRisk = StringField(propertyName="erosionRisk", name=EROSION_RISK)
EstimatedCapacity = MeasureField(propertyName="estimatedCapacity", name=ESTIMATED_CAPACITY, dps=0)
EstimatedCapacityPerArea = MeasureField(propertyName="estimatedCapacityPerArea",
                                        name=ESTIMATED_CAPACITY_PER_AREA, dps=1)
FarGrazingRadius = MeasureField(propertyName="farGrazingRadius", name=FAR_GRAZING_RADIUS, defaultValue="5000.0", dps=0)
Fid = IdField("id", name=FID)
LandscapeClass = StringField(propertyName="landscapeClass", name=LANDSCAPE_CLASS)
LandType = IdField(propertyName="landType", name=LAND_TYPE)
LandTypeName = StringField(propertyName="landTypeName", name=LAND_TYPE_NAME)
Latitude = MeasureField(propertyName="featureLatitude", name=LATITUDE, defaultValue=float('NaN'), dps=2)
Length = MeasureField(propertyName="featureLength", name=LENGTH, dps=2)
Longitude = MeasureField(propertyName="featureLongitude", name=LONGITUDE, defaultValue=float('NaN'), dps=2)
MapUnit = StringField(propertyName="mapUnit", name=MAP_UNIT)
Name = StringField(propertyName="name", name=NAME)
NearGrazingRadius = MeasureField(
    propertyName="nearGrazingRadius",
    name=NEAR_GRAZING_RADIUS,
    defaultValue="3000.0",
    dps=0)
OptimalCapacityPerArea = MeasureField(propertyName="optimalCapacityPerArea",
                                      name=OPTIMAL_CAPACITY_PER_AREA, dps=1)
Paddock = IdField(propertyName="paddock", name=PADDOCK)
PaddockName = StringField(propertyName="paddockName", name=PADDOCK_NAME)
PaddockStatus = DomainField(
    propertyName="paddockStatus",
    name=PADDOCK_STATUS,
    domainType=FeatureStatus,
    defaultValue=FeatureStatus.Undefined)
Perimeter = MeasureField(propertyName="featurePerimeter", name=PERIMETER, dps=2)
PotentialCapacity = MeasureField(propertyName="potentialCapacity", name=POTENTIAL_CAPACITY, dps=0)
PotentialCapacityPerArea = MeasureField(propertyName="potentialCapacityPerArea",
                                        name=POTENTIAL_CAPACITY_PER_AREA, dps=1)
Reference = StringField(propertyName="reference", name=REFERENCE)
Status = DomainField(propertyName="status", name=STATUS, domainType=FeatureStatus, defaultValue=FeatureStatus.Undefined)
TimeframeField = DomainField(
    propertyName="timeframe",
    name=TIMEFRAME,
    domainType=Timeframe,
    defaultValue=Timeframe.Undefined)
WateredArea = MeasureField(propertyName="wateredArea", name=WATERED_AREA, dps=2)
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
