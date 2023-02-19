# -*- coding: utf-8 -*-
from .calculator import Calculator
from .features import WateredArea
from .fields import FID, PADDOCK, STATUS, GRAZING_RADIUS_TYPE, TIMEFRAME, WATERED_TYPE, GrazingRadiusType, Timeframe, WateredType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWateredAreaLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Watered Areas"
    STYLE = "watered_area"

    @classmethod
    def getFeatureType(cls):
        return WateredArea

    def prepareQuery(self, query, *dependentLayers):
        [basePaddockLayer, waterpointBufferLayer] = self.names(*dependentLayers)

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
	st_multi(geometry) as geometry,
	0 as {FID},
 	{_NEAR_WATERED_AREA}.{PADDOCK},
  	'{WateredType.Near.name}' as {WATERED_TYPE},
	{_NEAR_WATERED_AREA}.{TIMEFRAME}
from {_NEAR_WATERED_AREA}
union
select
	st_multi(st_difference({_FAR_WATERED_AREA}.geometry, {_NEAR_WATERED_AREA}.geometry)) as geometry,
	0 as {FID},
	{_FAR_WATERED_AREA}.{PADDOCK},
 	'{WateredType.Far.name}' as {WATERED_TYPE},
 	{_FAR_WATERED_AREA}.{TIMEFRAME}
from {_FAR_WATERED_AREA}
inner join {_NEAR_WATERED_AREA}
	on {_FAR_WATERED_AREA}.{PADDOCK} = {_NEAR_WATERED_AREA}.{PADDOCK}
	and {_FAR_WATERED_AREA}.{TIMEFRAME} = {_NEAR_WATERED_AREA}.{TIMEFRAME}
	and st_difference({_FAR_WATERED_AREA}.geometry, {_NEAR_WATERED_AREA}.geometry) is not null
	and st_area(st_difference({_FAR_WATERED_AREA}.geometry, {_NEAR_WATERED_AREA}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
union
select
	st_multi(st_difference("{basePaddockLayer}".geometry, {_FAR_WATERED_AREA}.geometry)) as geometry,
	0 as {FID},
	{_FAR_WATERED_AREA}.{PADDOCK},
 	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	{_FAR_WATERED_AREA}.{TIMEFRAME}
from "{basePaddockLayer}"
inner join {_FAR_WATERED_AREA}
	on "{basePaddockLayer}".{FID} = {_FAR_WATERED_AREA}.{PADDOCK}
	and st_difference("{basePaddockLayer}".geometry, {_FAR_WATERED_AREA}.geometry) is not null
	and st_area(st_difference("{basePaddockLayer}".geometry, {_FAR_WATERED_AREA}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	and {Timeframe.timeframesIncludeStatuses(f'"{_FAR_WATERED_AREA}"."{TIMEFRAME}"', f'"{basePaddockLayer}"."{STATUS}"')}
union
select
	st_multi("{basePaddockLayer}".geometry) as geometry,
	0 as {FID},
 	"{basePaddockLayer}".{FID} as {PADDOCK},
  	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	'{Timeframe.Current.name}' as {TIMEFRAME}
from "{basePaddockLayer}" left join "{waterpointBufferLayer}"
where not exists (
	select 1
	from "{waterpointBufferLayer}"
	where "{waterpointBufferLayer}".{PADDOCK} = "{basePaddockLayer}".{FID}
	and {Timeframe.Current.timeframeIncludesStatuses(f'"{waterpointBufferLayer}".{TIMEFRAME}', f'"{basePaddockLayer}".{STATUS}')})
union
select
	st_multi("{basePaddockLayer}".geometry) as geometry,
	0 as {FID},
 	"{basePaddockLayer}".{FID} as {PADDOCK},
  	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	'{Timeframe.Future.name}' as {TIMEFRAME}
from "{basePaddockLayer}" left join "{waterpointBufferLayer}"
where not exists (
	select 1
	from "{waterpointBufferLayer}"
	where "{waterpointBufferLayer}".{PADDOCK} = "{basePaddockLayer}".{FID}
	and {Timeframe.Future.timeframeIncludesStatuses(f'"{waterpointBufferLayer}".{TIMEFRAME}', f'"{basePaddockLayer}".{STATUS}')})

"""
        return super().prepareQuery(query, *dependentLayers)

    def __init__(self,
                 basePaddockLayer,
                 waterpointBufferLayer):

        super().__init__(
            DerivedWateredAreaLayer.defaultName(),
            DerivedWateredAreaLayer.defaultStyle(),
            basePaddockLayer,
            waterpointBufferLayer)
