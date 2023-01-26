# -*- coding: utf-8 -*-
from ..calculator import Calculator
from ..features.waterpoint_buffer import WaterpointBuffer
from ..fields.names import FAR_GRAZING_RADIUS, FID, GRAZING_RADIUS, GRAZING_RADIUS_TYPE, NEAR_GRAZING_RADIUS, PADDOCK, STATUS, TIMEFRAME, WATERPOINT, WATERPOINT_TYPE
from ..fields.grazing_radius_type import GrazingRadiusType
from ..fields.timeframe import Timeframe
from ..fields.waterpoint_type import WaterpointType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWaterpointBufferLayer(DerivedFeatureLayer):

    STYLE = "waterpoint_buffer"

    def parameteriseQuery(self, PaddockLayer, WaterpointLayer):
        Buffers = "Buffers"
        FarBuffer = "FarBuffer"
        NearBuffer = "NearBuffer"
        InPaddocks = "InPaddocks"
        RenamedWaterpoints = "RenamedWaterpoints"

        return f"""
with {InPaddocks} as
    (select
        "{PaddockLayer}".geometry,
        "{PaddockLayer}".{FID} as "{PADDOCK}",
        "{WaterpointLayer}".{FID} as "{WATERPOINT}",
        '{Timeframe.Current.name}' as "{TIMEFRAME}"
	 from "{WaterpointLayer}"
	 inner join "{PaddockLayer}"
     on {Timeframe.Current.includesStatuses(f'"{WaterpointLayer}"."{STATUS}"', f'"{PaddockLayer}"."{STATUS}"')}
	 and st_contains("{PaddockLayer}".geometry, "{WaterpointLayer}".geometry)
     where {WaterpointType.givesWater(f'"{WaterpointLayer}"."{WATERPOINT_TYPE}"')}
     union
     select
        "{PaddockLayer}".geometry,
        "{PaddockLayer}".{FID} as "{PADDOCK}",
        "{WaterpointLayer}".{FID} as "{WATERPOINT}",
        '{Timeframe.Future.name}' as "{TIMEFRAME}"
	 from "{WaterpointLayer}"
	 inner join "{PaddockLayer}"
     on {Timeframe.Future.includesStatuses(f'"{WaterpointLayer}"."{STATUS}"', f'"{PaddockLayer}"."{STATUS}"')}
	 and st_contains("{PaddockLayer}".geometry, "{WaterpointLayer}".geometry)
     where {WaterpointType.givesWater(f'"{WaterpointLayer}"."{WATERPOINT_TYPE}"')}
     ),
{RenamedWaterpoints} as
     (select
	     geometry,
		 {STATUS},
		 {FID},
		 "{NEAR_GRAZING_RADIUS}" as {NearBuffer},
		 "{FAR_GRAZING_RADIUS}" as {FarBuffer}
	  from "{WaterpointLayer}"
      where {WaterpointType.givesWater(f'"{WaterpointLayer}"."{WATERPOINT_TYPE}"')}
      ),
{Buffers} as
    (select
		st_buffer(geometry, {NearBuffer}) as geometry,
		{FID} as "{WATERPOINT}",
        {STATUS},
        '{GrazingRadiusType.Near.name}' as "{GRAZING_RADIUS_TYPE}",
        {NearBuffer} as "{GRAZING_RADIUS}"
	 from {RenamedWaterpoints}
	 union
     select
		st_buffer(geometry, {FarBuffer}) as geometry,
		{FID} as "{WATERPOINT}",
        {STATUS},
        '{GrazingRadiusType.Far.name}' as "{GRAZING_RADIUS_TYPE}",
        {FarBuffer} as "{GRAZING_RADIUS}"
	 from {RenamedWaterpoints})
select
    0 as {FID},
    st_multi(st_intersection({Buffers}.geometry, {InPaddocks}.geometry)) as geometry,
    {InPaddocks}."{PADDOCK}",
    {InPaddocks}.{TIMEFRAME},
    {Buffers}.{STATUS},
    {Buffers}."{WATERPOINT}",
    {Buffers}."{GRAZING_RADIUS_TYPE}",
    {Buffers}."{GRAZING_RADIUS}"
from {Buffers}
inner join {InPaddocks}
on {Buffers}."{WATERPOINT}" = {InPaddocks}."{WATERPOINT}"
and st_area(st_intersection({Buffers}.geometry, {InPaddocks}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
and {Timeframe.timeframesIncludeStatuses(f'{InPaddocks}."{TIMEFRAME}"', f'{Buffers}."{STATUS}"')}
"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WaterpointBuffer

    def __init__(self, project, layerName, waterpointLayer, paddockLayer):
        super().__init__(
            project,
            layerName,
            self.parameteriseQuery(paddockLayer.name(), waterpointLayer.name()),
            DerivedWaterpointBufferLayer.STYLE,
            waterpointLayer,
            paddockLayer)
