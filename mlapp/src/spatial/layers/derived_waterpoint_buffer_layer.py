# -*- coding: utf-8 -*-
from ..features.waterpoint_buffer import WaterpointBuffer
from ..schemas.feature_status import FeatureStatus
from ..schemas.schemas import FAR_GRAZING_RADIUS, FID, GRAZING_RADIUS, GRAZING_RADIUS_TYPE, NEAR_GRAZING_RADIUS, STATUS, WATERPOINT, WATERPOINT_TYPE
from ..schemas.grazing_radius_type import GrazingRadiusType
from ..schemas.waterpoint_type import WaterpointType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWaterpointBufferLayer(DerivedFeatureLayer):

    STYLE = "waterpoint_buffer"

    QUERY = f"""
with "InPaddocks" as
    (select
        "{{1}}".geometry,
        "{{0}}".fid as "{WATERPOINT}"
	 from "{{0}}"
	 inner join "{{1}}"
	 on "{{0}}"."{STATUS}" in ('{FeatureStatus.Planned.name}', '{FeatureStatus.Built.name}')
	 and st_contains("{{1}}".geometry, "{{0}}".geometry)
     where "{{0}}"."{WATERPOINT_TYPE}" in ('{WaterpointType.Dam.name}', '{WaterpointType.Trough.name}', '{WaterpointType.Waterhole.name}')
     ),
"Renamed" as
     (select
	     geometry,
		 {STATUS},
		 fid,
		 "{NEAR_GRAZING_RADIUS}" as NearBuffer,
		 "{FAR_GRAZING_RADIUS}" as FarBuffer
	  from "{{0}}"),
"Buffers" as
    (select
		st_buffer(geometry, NearBuffer) as geometry,
		fid as "{WATERPOINT}",
        {STATUS},
        '{GrazingRadiusType.Near.name}' as "{GRAZING_RADIUS_TYPE}",
        NearBuffer as "{GRAZING_RADIUS}"
	 from "Renamed"
	 union
     select
		st_buffer(geometry, FarBuffer) as geometry,
		fid as "{WATERPOINT}",
        {STATUS},
        '{GrazingRadiusType.Far.name}' as "{GRAZING_RADIUS_TYPE}",
        FarBuffer as "{GRAZING_RADIUS}"
	 from "Renamed")
select
    0 as "{FID}",
    st_multi(st_intersection("Buffers".geometry, "InPaddocks".geometry)) as geometry,
    "Buffers"."{WATERPOINT}",
    {STATUS},
    "{GRAZING_RADIUS_TYPE}",
    "{GRAZING_RADIUS}"
from "Buffers"
inner join "InPaddocks"
on "Buffers"."{WATERPOINT}" = "InPaddocks"."{WATERPOINT}";
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WaterpointBuffer

    def __init__(self, layerName, waterpointLayer, paddockLayer):
        super().__init__(
            layerName,
            DerivedWaterpointBufferLayer.QUERY,
            DerivedWaterpointBufferLayer.STYLE,
            waterpointLayer,
            paddockLayer)
