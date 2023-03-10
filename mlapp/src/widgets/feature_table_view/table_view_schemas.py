# -*- coding: utf-8 -*-
from ...layers.fields.fields import *
from ...layers.fields import Schema

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

WaterpointTableViewSchema = Schema([DefaultTitle,
                                    WaterpointTypeField,
                                    Status,
                                    NearGrazingRadius,
                                    FarGrazingRadius,
                                    Longitude,
                                    Latitude,
                                    Elevation])
