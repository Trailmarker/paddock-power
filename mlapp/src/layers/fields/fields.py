# -*- coding: utf-8 -*-
from .names import *

from .condition_type import ConditionType
from .feature_status import FeatureStatus
from .field import CalculatedField, DomainField, IdField, MeasureField, StringField
from .timeframe import Timeframe
from .watered_type import WateredType
from .grazing_radius_type import GrazingRadiusType
from .waterpoint_type import WaterpointType


Area = CalculatedField(propertyName="AREA", name=AREA, dps=2)
BoreReportUrl = StringField(propertyName="BORE_REPORT_URL", name=BORE_REPORT_URL)
BoreYield = MeasureField(propertyName="BORE_YIELD", name=BORE_YIELD)
GrazingRadius = MeasureField(propertyName="GRAZING_RADIUS", name=GRAZING_RADIUS, dps=0)
BuildFence = IdField(propertyName="BUILD_FENCE", name=BUILD_FENCE)
BuildOrder = IdField(propertyName="BUILD_ORDER", name=BUILD_ORDER)
ClassDescription = StringField(propertyName="CLASS_DESCRIPTION", name=CLASS_DESCRIPTION)
ConditionTypeField = DomainField(
    propertyName="CONDITION_TYPE",
    name=CONDITION_TYPE,
    domainType=ConditionType,
    defaultValue=ConditionType.A)
Elevation = CalculatedField(propertyName="ELEVATION", name=ELEVATION, defaultValue=float('NaN'), dps=1)
ErosionRisk = StringField(propertyName="EROSION_RISK", name=EROSION_RISK)
EstimatedCapacity = CalculatedField(propertyName="ESTIMATED_CAPACITY", name=ESTIMATED_CAPACITY, dps=0)
EstimatedCapacityPerArea = CalculatedField(propertyName="ESTIMATED_CAPACITY_PER_AREA",
                                           name=ESTIMATED_CAPACITY_PER_AREA, dps=1)
FarGrazingRadius = MeasureField(
    propertyName="FAR_GRAZING_RADIUS",
    name=FAR_GRAZING_RADIUS,
    defaultValue="5000.0",
    dps=0)
Fid = IdField("FID", name=FID)
LandscapeClass = StringField(propertyName="LANDSCAPE_CLASS", name=LANDSCAPE_CLASS)
LandType = IdField(propertyName="LAND_TYPE", name=LAND_TYPE)
LandTypeName = StringField(propertyName="LAND_TYPE_NAME", name=LAND_TYPE_NAME, required=True)
Latitude = CalculatedField(propertyName="LATITUDE", name=LATITUDE, defaultValue=float('NaN'), dps=5)
Length = CalculatedField(propertyName="LENGTH", name=LENGTH, dps=2)
Longitude = CalculatedField(propertyName="LONGITUDE", name=LONGITUDE, defaultValue=float('NaN'), dps=5)
MapUnit = StringField(propertyName="MAP_UNIT", name=MAP_UNIT)
Name = StringField(propertyName="NAME", name=NAME, sortable=True)
NearGrazingRadius = MeasureField(
    propertyName="NEAR_GRAZING_RADIUS",
    name=NEAR_GRAZING_RADIUS,
    defaultValue="3000.0",
    dps=0)
OptimalCapacityPerArea = MeasureField(propertyName="OPTIMAL_CAPACITY_PER_AREA",
                                      name=OPTIMAL_CAPACITY_PER_AREA, defaultValue=0.0, dps=1, required=False)
Paddock = IdField(propertyName="PADDOCK", name=PADDOCK)
PaddockName = StringField(propertyName="PADDOCK_NAME", name=PADDOCK_NAME, sortable=True)
PaddockStatus = DomainField(
    propertyName="PADDOCK_STATUS",
    name=PADDOCK_STATUS,
    domainType=FeatureStatus,
    defaultValue=FeatureStatus.Undefined)
Perimeter = CalculatedField(propertyName="PERIMETER", name=PERIMETER, dps=2)
PotentialCapacity = CalculatedField(propertyName="POTENTIAL_CAPACITY", name=POTENTIAL_CAPACITY, dps=0)
PotentialCapacityPerArea = CalculatedField(propertyName="POTENTIAL_CAPACITY_PER_AREA",
                                           name=POTENTIAL_CAPACITY_PER_AREA, dps=1)
Reference = StringField(propertyName="REFERENCE", name=REFERENCE)
RequiredName = StringField(propertyName="NAME", name=NAME, required=True)
Status = DomainField(propertyName="STATUS", name=STATUS, domainType=FeatureStatus, defaultValue=FeatureStatus.Undefined)
TimeframeField = DomainField(
    propertyName="TIMEFRAME",
    name=TIMEFRAME,
    domainType=Timeframe,
    defaultValue=Timeframe.Undefined)
WateredArea = CalculatedField(propertyName="WATERED_AREA", name=WATERED_AREA, dps=2)
WateredTypeField = DomainField(
    propertyName="WATERED_TYPE",
    name=WATERED_TYPE,
    domainType=WateredType,
    defaultValue=WateredType.Unwatered)
Waterpoint = IdField(propertyName="WATERPOINT", name=WATERPOINT)
WaterpointName = StringField(propertyName="WATERPOINT_NAME", name=WATERPOINT_NAME)
GrazingRadiusTypeField = DomainField(
    propertyName="GRAZING_RADIUS_TYPE",
    name=GRAZING_RADIUS_TYPE,
    domainType=GrazingRadiusType)
WaterpointEndMonth = StringField(propertyName="WATERPOINT_END_MONTH", name=WATERPOINT_END_MONTH)
WaterpointStartMonth = StringField(propertyName="WATERPOINT_START_MONTH", name=WATERPOINT_START_MONTH)
WaterpointTypeField = DomainField(
    propertyName="WATERPOINT_TYPE",
    name=WATERPOINT_TYPE,
    domainType=WaterpointType,
    defaultValue=WaterpointType.Trough)
