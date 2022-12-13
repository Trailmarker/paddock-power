# -*- coding: utf-8 -*-
from ..features.waterpoint_buffer import WaterpointBuffer
from ..schemas.feature_status import FeatureStatus
from ..schemas.schemas import BUFFER_DISTANCE, FAR_BUFFER, NEAR_BUFFER, STATUS, WATERPOINT, WATERPOINT_BUFFER_TYPE, FeatureSchema
from ..schemas.waterpoint_buffer_type import WaterpointBufferType
from .derived_feature_layer import DerivedFeatureLayer


class WaterpointBufferLayer(DerivedFeatureLayer):

    STYLE = "waterpoint_buffer"


    QUERY = f"""
with "InPaddocks" as
    (select
        "{{1}}".geometry,
        "{{0}}".fid as "{WATERPOINT}"
	 from "{{0}}"
	 inner join "{{1}}"
	 on "{{0}}"."{STATUS}" in ('{FeatureStatus.Planned.name}', '{FeatureStatus.Built.name}')
	 and st_contains("{{1}}".geometry, "{{0}}".geometry)),
"Renamed" as
     (select
	     geometry,
		 {STATUS},
		 fid,
		 "{NEAR_BUFFER}" as NearBuffer,
		 "{FAR_BUFFER}" as FarBuffer
	  from "{{0}}"),
"Buffers" as
    (select 
		st_buffer(geometry, NearBuffer) as geometry,
		fid as "{WATERPOINT}",
        {STATUS},
        '{WaterpointBufferType.Near.name}' as "{WATERPOINT_BUFFER_TYPE}",
        NearBuffer as "{BUFFER_DISTANCE}"
	 from "Renamed"
	 union
     select
		st_buffer(geometry, FarBuffer) as geometry,
		fid as "{WATERPOINT}",
        {STATUS},
        '{WaterpointBufferType.Far.name}' as "{WATERPOINT_BUFFER_TYPE}",
        FarBuffer as "{BUFFER_DISTANCE}"
	 from "Renamed")
select
    st_intersection("Buffers".geometry, "InPaddocks".geometry) as geometry,
    "Buffers"."{WATERPOINT}",
    {STATUS},
    "{WATERPOINT_BUFFER_TYPE}",
    "{BUFFER_DISTANCE}"
from "Buffers"
inner join "InPaddocks"
on "Buffers"."{WATERPOINT}" = "InPaddocks"."{WATERPOINT}";
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WaterpointBuffer

    def __init__(self, layerName, waterpointLayer, paddockLayer):
        super().__init__(layerName, WaterpointBufferLayer.QUERY, WaterpointBufferLayer.STYLE, waterpointLayer, paddockLayer)
