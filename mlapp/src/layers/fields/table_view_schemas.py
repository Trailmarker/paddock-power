# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from .fields import *
from .schema import Schema

FenceTableViewSchema = Schema([LengthTitle,
                               BuildOrder,
                               Status,
                               Length])
# PaddockLandTypeSchema = Schema([Fid,
#                                 Paddock,
#                                 LandType,
#                                 PaddockName,
#                                 LandTypeName,
#                                 ConditionTypeField,
#                                 TimeframeField,
#                                 Area,
#                                 WateredArea,
#                                 EstimatedCapacityPerArea,
#                                 PotentialCapacityPerArea,
#                                 EstimatedCapacity,
#                                 PotentialCapacity],
#                                wkbType=QgsWkbTypes.MultiPolygon)
PaddockTableViewSchema = Schema([AreaTitle,
                                 Status,
                                 WateredArea,
                                 EstimatedCapacityPerArea,
                                 EstimatedCapacity,
                                 PotentialCapacityPerArea,
                                 PotentialCapacity])
PipelineTableViewSchema = Schema([LengthTitle,
                                  Status])
WaterpointTableViewSchema = Schema([DefaultTitle,
                                    WaterpointTypeField,
                                    Status,
                                    NearGrazingRadius,
                                    FarGrazingRadius,
                                    Longitude,
                                    Latitude,
                                    Elevation])
