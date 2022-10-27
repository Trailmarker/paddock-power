# -*- coding: utf-8 -*-
from ..features.waterpoint_buffer import WaterpointBuffer
from ..schemas.feature_status import FeatureStatus
from ..schemas.schemas import BUFFER_DISTANCE, FAR_BUFFER, NEAR_BUFFER, STATUS, WATERPOINT, WATERPOINT_BUFFER_TYPE, FeatureSchema
from ..schemas.waterpoint_buffer_type import WaterpointBufferType
from .derived_layer import DerivedLayer


class WaterpointBufferLayer(DerivedLayer):

    STYLE = "waterpoint_buffer_new_2"

    QUERY = f"""
with "Buffers" as
    (select
     st_buffer(geometry, "{NEAR_BUFFER}") as "Near",
     st_buffer(geometry, "{FAR_BUFFER}") as "Far",
     fid as "{WATERPOINT}",
     "{STATUS}",
     "{NEAR_BUFFER}",
     "{FAR_BUFFER}"
     from {{0}}
     where "{STATUS}" in ('{FeatureStatus.Planned.name}', '{FeatureStatus.Built.name}'))
select
    "Near" as "geometry",
    "{WATERPOINT}",
    '{WaterpointBufferType.Near.name}' as "{WATERPOINT_BUFFER_TYPE}",
    "{STATUS}",
    "{NEAR_BUFFER}" as "{BUFFER_DISTANCE}"
from "Buffers"
union
select
    st_difference("Far", "Near") as "geometry",
    "{WATERPOINT}",
    '{WaterpointBufferType.Far.name}' as "{WATERPOINT_BUFFER_TYPE}",
    "{STATUS}",
    "{FAR_BUFFER}" as "{BUFFER_DISTANCE}"
from "Buffers"
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WaterpointBuffer

    def __init__(self, layerName, waterpointLayer):
        super().__init__(layerName, WaterpointBufferLayer.QUERY, WaterpointBufferLayer.STYLE, waterpointLayer)
