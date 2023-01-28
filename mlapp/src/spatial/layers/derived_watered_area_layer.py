# -*- coding: utf-8 -*-
from ..calculator import Calculator
from ..features.watered_area import WateredArea
from ..fields.grazing_radius_type import GrazingRadiusType
from ..fields.names import FID, PADDOCK, STATUS, GRAZING_RADIUS_TYPE, TIMEFRAME, WATERED_TYPE
from ..fields.timeframe import Timeframe
from ..fields.watered_type import WateredType
from .derived_feature_layer import DerivedFeatureLayer
from .paddock_layer import PaddockLayer
from .waterpoint_buffer_layer import WaterpointBufferLayer

class DerivedWateredAreaLayer(DerivedFeatureLayer):

    NAME = "Derived Watered Areas"
    STYLE = "watered_area"

    def prepareQuery(self, query=None, *dependentLayers):
        [paddockLayer, waterpointBufferLayer] = self.names(*dependentLayers)
        
        _NEAR_WATERED_AREA = "NearWateredArea"
        _FAR_WATERED_AREA = "FarWateredArea"

        query = f"""
with
  {_NEAR_WATERED_AREA} as
	(select
		st_union(geometry) as geometry,
		{PADDOCK},
		{TIMEFRAME}
	 from "{waterpointBufferLayer}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Near.name}'
	 group by {PADDOCK}, {TIMEFRAME})
, {_FAR_WATERED_AREA} as
	(select
		st_union(geometry) as geometry,
		{PADDOCK},
		{TIMEFRAME}
	 from "{waterpointBufferLayer}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Far.name}'
	 group by {PADDOCK}, {TIMEFRAME})
select
	0 as {FID},
	st_multi(geometry) as geometry,
	'{WateredType.Near.name}' as {WATERED_TYPE},
	{_NEAR_WATERED_AREA}.{TIMEFRAME},
	{_NEAR_WATERED_AREA}.{PADDOCK}
from {_NEAR_WATERED_AREA}
union
select
	0 as {FID},
	st_multi(st_difference({_FAR_WATERED_AREA}.geometry, {_NEAR_WATERED_AREA}.geometry)) as geometry,
	'{WateredType.Far.name}' as {WATERED_TYPE},
	{_FAR_WATERED_AREA}.{TIMEFRAME},
	{_FAR_WATERED_AREA}.{PADDOCK}
from {_FAR_WATERED_AREA}
inner join {_NEAR_WATERED_AREA}
	on {_FAR_WATERED_AREA}.{TIMEFRAME} = {_NEAR_WATERED_AREA}.{TIMEFRAME}
	and {_FAR_WATERED_AREA}.{PADDOCK} = {_NEAR_WATERED_AREA}.{PADDOCK}
	and st_difference({_FAR_WATERED_AREA}.geometry, {_NEAR_WATERED_AREA}.geometry) is not null
	and st_area(st_difference({_FAR_WATERED_AREA}.geometry, {_NEAR_WATERED_AREA}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
union
select
	0 as {FID},
	st_multi(st_difference({paddockLayer}.geometry, {_FAR_WATERED_AREA}.geometry)) as geometry,
	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	{_FAR_WATERED_AREA}.{TIMEFRAME},
	{_FAR_WATERED_AREA}.{PADDOCK}
from "{paddockLayer}"
inner join {_FAR_WATERED_AREA}
	on "{paddockLayer}".{FID} = {_FAR_WATERED_AREA}.{PADDOCK}
	and st_difference({paddockLayer}.geometry, {_FAR_WATERED_AREA}.geometry) is not null
	and st_area(st_difference({paddockLayer}.geometry, {_FAR_WATERED_AREA}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	and {Timeframe.timeframesIncludeStatuses(f'"{_FAR_WATERED_AREA}"."{TIMEFRAME}"', f'"{paddockLayer}"."{STATUS}"')}
union
select
	0 as {FID},
	st_multi({paddockLayer}.geometry) as geometry,
	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	'{Timeframe.Current.name}' as {TIMEFRAME},
	"{paddockLayer}".{FID} as {PADDOCK}
from "{paddockLayer}" left join "{waterpointBufferLayer}"
where not exists (
	select 1
	from "{waterpointBufferLayer}"
	where "{waterpointBufferLayer}".{PADDOCK} = "{paddockLayer}".{FID}
	and {Timeframe.Current.timeframeIncludesStatuses(f'"{waterpointBufferLayer}".{TIMEFRAME}', f'"{paddockLayer}".{STATUS}')})
union
select
	0 as {FID},
	st_multi({paddockLayer}.geometry) as geometry,
	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	'{Timeframe.Future.name}' as {TIMEFRAME},
	"{paddockLayer}".{FID} as {PADDOCK}
from "{paddockLayer}" left join "{waterpointBufferLayer}"
where not exists (
	select 1
	from "{waterpointBufferLayer}"
	where "{waterpointBufferLayer}".{PADDOCK} = "{paddockLayer}".{FID}
	and {Timeframe.Future.timeframeIncludesStatuses(f'"{waterpointBufferLayer}".{TIMEFRAME}', f'"{paddockLayer}".{STATUS}')})

"""
        return super().prepareQuery(query, *dependentLayers)

    def __init__(self,
                 paddockLayer: PaddockLayer,
                 waterpointBufferLayer: WaterpointBufferLayer):
        
        super().__init__(WateredArea,
                         DerivedWateredAreaLayer.NAME,
                         DerivedWateredAreaLayer.STYLE,
                         paddockLayer,
                         waterpointBufferLayer)
        
