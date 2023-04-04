# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from .fields import *
from .schema import Schema

PropertySchema = Schema([Fid,
                         TimeframeField,
                         Perimeter,
                         Area,
                         WateredArea,
                         EstimatedCapacityPerArea,
                         PotentialCapacityPerArea,
                         EstimatedCapacity,
                         PotentialCapacity],
                        wkbType=QgsWkbTypes.MultiPolygon,
                        hiddenFields=[Fid,
                                      EstimatedCapacityPerArea,
                                      PotentialCapacityPerArea])
FeatureSchema = Schema([Fid])
FenceSchema = Schema([Fid,
                      Name,
                      BuildOrder,
                      Status,
                      Length],
                     wkbType=QgsWkbTypes.LineString,
                     hiddenFields=[Fid])
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
                           wkbType=QgsWkbTypes.MultiPolygon,
                           hiddenFields=[Fid, BuildFence, Perimeter])
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
                               wkbType=QgsWkbTypes.MultiPolygon,
                               hiddenFields=[Fid,
                                             Paddock,
                                             LandType,
                                             PaddockName,
                                             TimeframeField,
                                             Area,
                                             EstimatedCapacityPerArea,
                                             PotentialCapacityPerArea])
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
                              PotentialCapacityPerArea,
                              EstimatedCapacity,
                              PotentialCapacity],
                             wkbType=QgsWkbTypes.MultiPolygon,
                             hiddenFields=[Fid,
                                           Paddock,
                                           BuildFence,
                                           TimeframeField,
                                           Perimeter,
                                           EstimatedCapacityPerArea,
                                           PotentialCapacityPerArea])
PipelineSchema = Schema([Fid,
                         Name,
                         Status,
                         Length],
                        wkbType=QgsWkbTypes.LineString,
                        hiddenFields=[Fid])
StatusFeatureSchema = Schema([Fid,
                              Name,
                              Status])
WaterpointBufferSchema = Schema([Fid,
                                 Waterpoint,
                                 WaterpointName,
                                 Paddock,
                                 PaddockName,
                                 GrazingRadiusTypeField,
                                 GrazingRadius,
                                 Status,
                                 TimeframeField,
                                 Area],
                                wkbType=QgsWkbTypes.MultiPolygon,
                                hiddenFields=[Fid,
                                              Waterpoint,
                                              Paddock])
WateredAreaSchema = Schema([Fid,
                            Paddock,
                            PaddockName,
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
