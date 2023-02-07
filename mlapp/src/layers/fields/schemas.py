# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from .fields import *
from .schema import Schema

BoundarySchema = Schema([Fid, TimeframeField], wkbType=QgsWkbTypes.MultiPolygon)
FeatureSchema = Schema([Fid])
FenceSchema = Schema([Fid, Name, Status, Length, BuildOrder], wkbType=QgsWkbTypes.LineString)
LandTypeSchema = Schema([Fid, LandTypeName, Area, Perimeter, OptimalCapacityPerArea, MapUnit, LandscapeClass,
                         ClassDescription, ErosionRisk], wkbType=QgsWkbTypes.MultiPolygon)
BasePaddockSchema = Schema([Fid,
                        Name,
                        Status,
                        Area,
                        Perimeter,
                        BuildFence],
                       wkbType=QgsWkbTypes.MultiPolygon)
PaddockLandTypeSchema = Schema([Fid,
                                Area,
                                WateredArea,
                                EstimatedCapacityPerArea,
                                PotentialCapacityPerArea,
                                EstimatedCapacity,
                                PotentialCapacity,
                                ConditionTypeField,
                                Paddock,
                                PaddockName,
                                LandType,
                                LandTypeName,
                                TimeframeField],
                               wkbType=QgsWkbTypes.MultiPolygon)
MetricPaddockSchema = Schema([Fid,
                              Paddock,
                              Name,
                              Status,
                              TimeframeField,
                              Area,
                              WateredArea,
                              Perimeter,
                              BuildFence,
                              EstimatedCapacityPerArea,
                              EstimatedCapacity,
                              PotentialCapacityPerArea,
                              PotentialCapacity],
                             wkbType=QgsWkbTypes.MultiPolygon)
PipelineSchema = Schema([Fid, Name, Status, Length], wkbType=QgsWkbTypes.LineString)
StatusFeatureSchema = Schema([Fid, Name, Status])
WaterpointBufferSchema = Schema(
    [Fid, TimeframeField, Paddock, Status, Waterpoint, GrazingRadiusTypeField, GrazingRadius],
    wkbType=QgsWkbTypes.MultiPolygon)
WateredAreaSchema = Schema([Fid, WateredTypeField, Paddock, TimeframeField], wkbType=QgsWkbTypes.MultiPolygon)
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
