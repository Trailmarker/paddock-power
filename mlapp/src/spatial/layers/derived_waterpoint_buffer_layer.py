# -*- coding: utf-8 -*-
from ..calculator import Calculator
from ..features.waterpoint_buffer import WaterpointBuffer
from ..schemas.feature_status import FeatureStatus
from ..schemas.schemas import FAR_GRAZING_RADIUS, FID, GRAZING_RADIUS, GRAZING_RADIUS_TYPE, NEAR_GRAZING_RADIUS, PADDOCK, PADDOCK_STATUS, STATUS, WATERPOINT, WATERPOINT_TYPE
from ..schemas.grazing_radius_type import GrazingRadiusType
from ..schemas.waterpoint_type import WaterpointType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWaterpointBufferLayer(DerivedFeatureLayer):

    STYLE = "waterpoint_buffer"

    BUFFERS = "Buffers"
    FAR_BUFFER = "FarBuffer"
    NEAR_BUFFER = "NearBuffer"
    IN_PADDOCKS = "InPaddocks"
    RENAMED_WATERPOINTS = "RenamedWaterpoints"

    QUERY = f"""
with "{IN_PADDOCKS}" as
    (select
        "{{1}}".geometry,
        "{{1}}".fid as "{PADDOCK}",
        "{{0}}".fid as "{WATERPOINT}",
        "{{1}}".{STATUS} as "{PADDOCK_STATUS}"
	 from "{{0}}"
	 inner join "{{1}}"
     on "{{0}}"."{STATUS}" in ('{FeatureStatus.Planned.name}', '{FeatureStatus.Built.name}')
	 and st_contains("{{1}}".geometry, "{{0}}".geometry)
     where "{{0}}"."{WATERPOINT_TYPE}" in ('{WaterpointType.Dam.name}', '{WaterpointType.Trough.name}', '{WaterpointType.Waterhole.name}')
     ),
"{RENAMED_WATERPOINTS}" as
     (select
	     geometry,
		 {STATUS},
		 fid,
		 "{NEAR_GRAZING_RADIUS}" as {NEAR_BUFFER},
		 "{FAR_GRAZING_RADIUS}" as {FAR_BUFFER}
	  from "{{0}}"
      where "{{0}}"."{WATERPOINT_TYPE}" in ('{WaterpointType.Dam.name}', '{WaterpointType.Trough.name}', '{WaterpointType.Waterhole.name}')),
"{BUFFERS}" as
    (select
		st_buffer(geometry, {NEAR_BUFFER}) as geometry,
		fid as "{WATERPOINT}",
        {STATUS},
        '{GrazingRadiusType.Near.name}' as "{GRAZING_RADIUS_TYPE}",
        {NEAR_BUFFER} as "{GRAZING_RADIUS}"
	 from "{RENAMED_WATERPOINTS}"
	 union
     select
		st_buffer(geometry, {FAR_BUFFER}) as geometry,
		fid as "{WATERPOINT}",
        {STATUS},
        '{GrazingRadiusType.Far.name}' as "{GRAZING_RADIUS_TYPE}",
        {FAR_BUFFER} as "{GRAZING_RADIUS}"
	 from "{RENAMED_WATERPOINTS}")
select
    0 as "{FID}",
    st_multi(st_intersection("{BUFFERS}".geometry, "{IN_PADDOCKS}".geometry)) as geometry,
    "{IN_PADDOCKS}"."{PADDOCK}",
    "{IN_PADDOCKS}"."{PADDOCK_STATUS}",
    "{BUFFERS}"."{WATERPOINT}",
    {STATUS},
    "{GRAZING_RADIUS_TYPE}",
    "{GRAZING_RADIUS}"
from "{BUFFERS}"
inner join "{IN_PADDOCKS}"
on "{BUFFERS}"."{WATERPOINT}" = "{IN_PADDOCKS}"."{WATERPOINT}"
and st_area(st_intersection("{BUFFERS}".geometry, "{IN_PADDOCKS}".geometry)) >= {Calculator.MINIMUM_AREA_M2}
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
