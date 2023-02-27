# -*- coding: utf-8 -*-
from ..utils import randomString
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

    def getRederiveFeaturesRequest(self):
        """Define which features must be removed from a target layer to be re-derived."""
        if not self.changeset:
            return None
        
        [basePaddockLayer, waterpointBufferLayer] = self.dependentLayers            
        return self.prepareRederiveFeaturesRequest(basePaddockLayer, PADDOCK, FID, waterpointBufferLayer, PADDOCK, PADDOCK)    

    def prepareQuery(self, query, dependentLayers):        
        [basePaddockLayer, waterpointBufferLayer] = dependentLayers
        [basePaddocks, waterpointBuffers] = self.names(dependentLayers)

  		# Set up clauses
        filterWaterpointBuffers = self.andAllKeyClauses(self.changeset, basePaddockLayer, PADDOCK, FID, waterpointBufferLayer, PADDOCK, PADDOCK)
        filterPaddocks = self.andAllKeyClauses(self.changeset, basePaddockLayer, FID, FID, waterpointBufferLayer, FID, PADDOCK)

        _NEAR_WATERED_AREA = f"NearWateredArea{randomString()}"
        _FAR_WATERED_AREA = f"FarWateredArea{randomString()}"
        _FILTERED_PADDOCKS = f"FilteredPaddocks{randomString()}"
        _UNWATERED_PADDOCKS = f"UnwateredPaddocks{randomString()}"

        query = f"""
with
  {_NEAR_WATERED_AREA} as
	(select
		st_union(geometry) as geometry,
		{PADDOCK},
		{TIMEFRAME}
	 from "{waterpointBuffers}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Near.name}'
	 {filterWaterpointBuffers}
	 group by {PADDOCK}, {TIMEFRAME})
, {_FAR_WATERED_AREA} as
	(select
		st_union(geometry) as geometry,
		{PADDOCK},
		{TIMEFRAME}
	 from "{waterpointBuffers}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Far.name}'
     {filterWaterpointBuffers}
	 group by {PADDOCK}, {TIMEFRAME})
, {_FILTERED_PADDOCKS} as
    (select * from "{basePaddocks}"
     where 1=1
     {filterPaddocks})
, {_UNWATERED_PADDOCKS} as
    (select
		st_multi("{_FILTERED_PADDOCKS}".geometry) as geometry,
		0 as {FID},
		"{_FILTERED_PADDOCKS}".{FID} as {PADDOCK},
		'{WateredType.Unwatered.name}' as {WATERED_TYPE},
		'{Timeframe.Current.name}' as {TIMEFRAME}
	 from "{_FILTERED_PADDOCKS}" left join "{waterpointBuffers}"
	 where not exists (
		select 1
		from "{waterpointBuffers}"
		where "{waterpointBuffers}".{PADDOCK} = "{_FILTERED_PADDOCKS}".{FID}
		and {Timeframe.Current.timeframeIncludesStatuses(f'"{waterpointBuffers}".{TIMEFRAME}', f'"{_FILTERED_PADDOCKS}".{STATUS}')})
	 union
	 select
		st_multi("{_FILTERED_PADDOCKS}".geometry) as geometry,
		0 as {FID},
		"{_FILTERED_PADDOCKS}".{FID} as {PADDOCK},
		'{WateredType.Unwatered.name}' as {WATERED_TYPE},
		'{Timeframe.Future.name}' as {TIMEFRAME}
	 from "{_FILTERED_PADDOCKS}" left join "{waterpointBuffers}"
	 where not exists (
		select 1
		from "{waterpointBuffers}"
		where "{waterpointBuffers}".{PADDOCK} = "{_FILTERED_PADDOCKS}".{FID}
		and {Timeframe.Future.timeframeIncludesStatuses(f'"{waterpointBuffers}".{TIMEFRAME}', f'"{_FILTERED_PADDOCKS}".{STATUS}')}))
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
	st_multi(st_difference("{_FILTERED_PADDOCKS}".geometry, {_FAR_WATERED_AREA}.geometry)) as geometry,
	0 as {FID},
	{_FAR_WATERED_AREA}.{PADDOCK},
 	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	{_FAR_WATERED_AREA}.{TIMEFRAME}
from "{_FILTERED_PADDOCKS}"
inner join {_FAR_WATERED_AREA}
	on "{_FILTERED_PADDOCKS}".{FID} = {_FAR_WATERED_AREA}.{PADDOCK}
	and st_difference("{_FILTERED_PADDOCKS}".geometry, {_FAR_WATERED_AREA}.geometry) is not null
	and st_area(st_difference("{_FILTERED_PADDOCKS}".geometry, {_FAR_WATERED_AREA}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	and {Timeframe.timeframesIncludeStatuses(f'"{_FAR_WATERED_AREA}"."{TIMEFRAME}"', f'"{_FILTERED_PADDOCKS}"."{STATUS}"')}
union
select * from {_UNWATERED_PADDOCKS}
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(
            DerivedWateredAreaLayer.defaultName(),
            DerivedWateredAreaLayer.defaultStyle(),
            dependentLayers,
            changeset)