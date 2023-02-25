# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from .fields import *
from .schema import Schema

BoundarySchema = Schema([Fid,
                         TimeframeField],
                        wkbType=QgsWkbTypes.MultiPolygon)
FeatureSchema = Schema([Fid])
FenceSchema = Schema([Fid,
                      Name,
                      BuildOrder,
                      Status,
                      Length],
                     wkbType=QgsWkbTypes.LineString)
LandTypeSchema = Schema([Fid,
                         LandTypeName,
                         OptimalCapacityPerArea,
                         Perimeter,
                         Area],
                        wkbType=QgsWkbTypes.MultiPolygon)
BasePaddockSchema = Schema([Fid,
                            Name,
                            BuildFence,
                            Status,
                            Perimeter,
                            Area],
                           wkbType=QgsWkbTypes.MultiPolygon)
PaddockLandTypeSchema = Schema([Fid,
                                Paddock,
                                LandType,
                                PaddockName,
                                LandTypeName,
                                ConditionTypeField,
                                TimeframeField,
                                Area,
                                WateredArea,
                                EstimatedCapacityPerArea,
                                PotentialCapacityPerArea,
                                EstimatedCapacity,
                                PotentialCapacity],
                               wkbType=QgsWkbTypes.MultiPolygon)
MetricPaddockSchema = Schema([Fid,
                              Paddock,
                              Name,
                              BuildFence,
                              Status,
                              TimeframeField,
                              Perimeter,
                              Area,
                              WateredArea,
                              EstimatedCapacityPerArea,
                              EstimatedCapacity,
                              PotentialCapacityPerArea,
                              PotentialCapacity],
                             wkbType=QgsWkbTypes.MultiPolygon)
PipelineSchema = Schema([Fid,
                         Name,
                         Status,
                         Length],
                        wkbType=QgsWkbTypes.LineString)
StatusFeatureSchema = Schema([Fid,
                              Name,
                              Status])
WaterpointBufferSchema = Schema([Fid,
                                 Waterpoint,
                                 Paddock,
                                 GrazingRadiusTypeField,
                                 GrazingRadius,
                                 Status,
                                 TimeframeField],
                                wkbType=QgsWkbTypes.MultiPolygon)
WateredAreaSchema = Schema([Fid,
                            Paddock,
                            WateredTypeField,
                            TimeframeField], wkbType=QgsWkbTypes.MultiPolygon)
WaterpointSchema = Schema([Fid,
                           Name,
                           WaterpointTypeField,
                           Status,
                           NearGrazingRadius,
                           FarGrazingRadius,
                           Longitude,
                           Latitude,
                           Elevation],
                          wkbType=QgsWkbTypes.Point)
