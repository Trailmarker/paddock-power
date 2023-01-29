# -*- coding: utf-8 -*-
from ..calculator import Calculator
from ..features.waterpoint_buffer import WaterpointBuffer
from ..fields.names import FAR_GRAZING_RADIUS, FID, GRAZING_RADIUS, GRAZING_RADIUS_TYPE, NEAR_GRAZING_RADIUS, PADDOCK, STATUS, TIMEFRAME, WATERPOINT, WATERPOINT_TYPE
from ..fields.grazing_radius_type import GrazingRadiusType
from ..fields.schemas import WaterpointBufferSchema
from ..fields.timeframe import Timeframe
from ..fields.waterpoint_type import WaterpointType
from .derived_feature_layer import DerivedFeatureLayer
from .paddock_layer import PaddockLayer
from .waterpoint_layer import WaterpointLayer

class DerivedWaterpointBufferLayer(DerivedFeatureLayer):

    NAME = "Derived Waterpoint Buffers"
    STYLE = "waterpoint_buffer"

    def prepareQuery(self, query, *dependentLayers):
        [paddockLayer, waterpointLayer] = self.names(*dependentLayers)
        
        _BUFFERS = "Buffers"
        _FAR_BUFFER = "FarBuffer"
        _NEAR_BUFFER = "NearBuffer"
        _IN_PADDOCKS = "InPaddocks"
        _RENAMED_WATERPOINTS = "RenamedWaterpoints"

        query = f"""
with {_IN_PADDOCKS} as
    (select
        "{paddockLayer}".geometry,
        "{paddockLayer}".{FID} as "{PADDOCK}",
        "{waterpointLayer}".{FID} as "{WATERPOINT}",
        '{Timeframe.Current.name}' as "{TIMEFRAME}"
	 from "{waterpointLayer}"
	 inner join "{paddockLayer}"
     on {Timeframe.Current.includesStatuses(f'"{waterpointLayer}"."{STATUS}"', f'"{paddockLayer}"."{STATUS}"')}
	 and st_contains("{paddockLayer}".geometry, "{waterpointLayer}".geometry)
     where {WaterpointType.givesWater(f'"{waterpointLayer}"."{WATERPOINT_TYPE}"')}
     union
     select
        "{paddockLayer}".geometry,
        "{paddockLayer}".{FID} as "{PADDOCK}",
        "{waterpointLayer}".{FID} as "{WATERPOINT}",
        '{Timeframe.Future.name}' as "{TIMEFRAME}"
	 from "{waterpointLayer}"
	 inner join "{paddockLayer}"
     on {Timeframe.Future.includesStatuses(f'"{waterpointLayer}"."{STATUS}"', f'"{paddockLayer}"."{STATUS}"')}
	 and st_contains("{paddockLayer}".geometry, "{waterpointLayer}".geometry)
     where {WaterpointType.givesWater(f'"{waterpointLayer}"."{WATERPOINT_TYPE}"')}
     ),
{_RENAMED_WATERPOINTS} as
     (select
	     geometry,
		 {STATUS},
		 {FID},
		 "{NEAR_GRAZING_RADIUS}" as {_NEAR_BUFFER},
		 "{FAR_GRAZING_RADIUS}" as {_FAR_BUFFER}
	  from "{waterpointLayer}"
      where {WaterpointType.givesWater(f'"{waterpointLayer}"."{WATERPOINT_TYPE}"')}
      ),
{_BUFFERS} as
    (select
		st_buffer(geometry, {_NEAR_BUFFER}) as geometry,
		{FID} as "{WATERPOINT}",
        {STATUS},
        '{GrazingRadiusType.Near.name}' as "{GRAZING_RADIUS_TYPE}",
        {_NEAR_BUFFER} as "{GRAZING_RADIUS}"
	 from {_RENAMED_WATERPOINTS}
	 union
     select
		st_buffer(geometry, {_FAR_BUFFER}) as geometry,
		{FID} as "{WATERPOINT}",
        {STATUS},
        '{GrazingRadiusType.Far.name}' as "{GRAZING_RADIUS_TYPE}",
        {_FAR_BUFFER} as "{GRAZING_RADIUS}"
	 from {_RENAMED_WATERPOINTS})
select
    0 as {FID},
    st_multi(st_intersection({_BUFFERS}.geometry, {_IN_PADDOCKS}.geometry)) as geometry,
    {_IN_PADDOCKS}."{PADDOCK}",
    {_IN_PADDOCKS}.{TIMEFRAME},
    {_BUFFERS}.{STATUS},
    {_BUFFERS}."{WATERPOINT}",
    {_BUFFERS}."{GRAZING_RADIUS_TYPE}",
    {_BUFFERS}."{GRAZING_RADIUS}"
from {_BUFFERS}
inner join {_IN_PADDOCKS}
on {_BUFFERS}."{WATERPOINT}" = {_IN_PADDOCKS}."{WATERPOINT}"
and st_area(st_intersection({_BUFFERS}.geometry, {_IN_PADDOCKS}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
and {Timeframe.timeframesIncludeStatuses(f'{_IN_PADDOCKS}."{TIMEFRAME}"', f'{_BUFFERS}."{STATUS}"')}
"""
        return super().prepareQuery(query, *dependentLayers)

    def __init__(self,
                 paddockLayer: PaddockLayer,
                 waterpointLayer: WaterpointLayer):
        
        super().__init__(
            WaterpointBuffer,
            DerivedWaterpointBufferLayer.NAME,
            DerivedWaterpointBufferLayer.STYLE,
            paddockLayer,
            waterpointLayer)


    def getSchema(self):
        """Return the Schema for this layer."""
        return WaterpointBufferSchema
        
    
    def getWkbType(self):
        """Return the WKB type for this layer."""
        return WaterpointBufferSchema.wkbType