# -*- coding: utf-8 -*-
from ..utils import randomString
from .calculator import Calculator
from .features import WateredArea
from .fields import FID, PADDOCK, STATUS, GRAZING_RADIUS_TYPE, NAME, PADDOCK_NAME, TIMEFRAME, WATERED_TYPE, GrazingRadiusType, Timeframe, WateredType
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

        [analyticPaddockLayer, waterpointBufferLayer] = self.dependentLayers
        return self.prepareRederiveFeaturesRequest(
            analyticPaddockLayer, PADDOCK, FID, waterpointBufferLayer, PADDOCK, PADDOCK)

    def prepareQuery(self, query, dependentLayers):
        [analyticPaddockLayer, waterpointBufferLayer] = dependentLayers
        [analyticPaddocks, waterpointBuffers] = self.names(dependentLayers)

        # Set up clauses
        filterWaterpointBuffers = self.andAllKeyClauses(
            self.changeset,
            analyticPaddockLayer,
            PADDOCK,
            FID,
            waterpointBufferLayer,
            PADDOCK,
            PADDOCK)
        filterPaddocks = self.andAllKeyClauses(
            self.changeset,
            analyticPaddockLayer,
            FID,
            FID,
            waterpointBufferLayer,
            FID,
            PADDOCK)

        _NEAR_WATERED_AREA = f"NearWateredArea{randomString()}"
        _FAR_WATERED_AREA = f"FarWateredArea{randomString()}"
        _FILTERED_PADDOCKS = f"FilteredPaddocks{randomString()}"
        _UNWATERED_PADDOCKS = f"UnwateredPaddocks{randomString()}"

        if filterPaddocks:
            _FILTERED_PADDOCKS = f"FilteredPaddocks{randomString()}"
            withFilteredPaddocks = f"""
  {_FILTERED_PADDOCKS} as
    (select * from "{analyticPaddocks}"
     where 1=1
     {filterPaddocks}),
"""
        else:
            _FILTERED_PADDOCKS = analyticPaddocks
            withFilteredPaddocks = ""
        query = f"""
with
  {withFilteredPaddocks}
  {_NEAR_WATERED_AREA} as
	(select
		st_union(geometry) as geometry,
		{PADDOCK},
        "{PADDOCK_NAME}",
		{TIMEFRAME}
	 from "{waterpointBuffers}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Near.name}'
	 {filterWaterpointBuffers}
	 group by {PADDOCK}, "{PADDOCK_NAME}", {TIMEFRAME}),
  {_FAR_WATERED_AREA} as
	(select
		st_union(geometry) as geometry,
		{PADDOCK},
        "{PADDOCK_NAME}",
		{TIMEFRAME}
	 from "{waterpointBuffers}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Far.name}'
     {filterWaterpointBuffers}
	 group by {PADDOCK}, "{PADDOCK_NAME}", {TIMEFRAME}),
  {_UNWATERED_PADDOCKS} as
    (select
		st_multi("{_FILTERED_PADDOCKS}".geometry) as geometry,
		0 as {FID},
		"{_FILTERED_PADDOCKS}".{PADDOCK} as {PADDOCK},
        "{_FILTERED_PADDOCKS}".{NAME} as "{PADDOCK_NAME}",
		'{WateredType.Unwatered.name}' as {WATERED_TYPE},
		'{Timeframe.Current.name}' as {TIMEFRAME}
	 from "{_FILTERED_PADDOCKS}" left join "{waterpointBuffers}"
	 where not exists (
		select 1
		from "{waterpointBuffers}"
		where "{waterpointBuffers}".{PADDOCK} = "{_FILTERED_PADDOCKS}".{FID}
		and {Timeframe.Current.timeframeMatchesStatuses(f'"{waterpointBuffers}".{TIMEFRAME}', f'"{_FILTERED_PADDOCKS}".{STATUS}')})
	 union
	 select
		st_multi("{_FILTERED_PADDOCKS}".geometry) as geometry,
		0 as {FID},
		"{_FILTERED_PADDOCKS}".{PADDOCK} as {PADDOCK},
        "{_FILTERED_PADDOCKS}".{NAME} as "{PADDOCK_NAME}",
		'{WateredType.Unwatered.name}' as {WATERED_TYPE},
		'{Timeframe.Future.name}' as {TIMEFRAME}
	 from "{_FILTERED_PADDOCKS}" left join "{waterpointBuffers}"
	 where not exists (
		select 1
		from "{waterpointBuffers}"
		where "{waterpointBuffers}".{PADDOCK} = "{_FILTERED_PADDOCKS}".{FID}
		and {Timeframe.Future.timeframeMatchesStatuses(f'"{waterpointBuffers}".{TIMEFRAME}', f'"{_FILTERED_PADDOCKS}".{STATUS}')}))
select
	st_multi(geometry) as geometry,
	0 as {FID},
 	{_NEAR_WATERED_AREA}.{PADDOCK},
    {_NEAR_WATERED_AREA}."{PADDOCK_NAME}",
  	'{WateredType.Near.name}' as {WATERED_TYPE},
	{_NEAR_WATERED_AREA}.{TIMEFRAME}
from {_NEAR_WATERED_AREA}
union
select
	st_multi(st_difference({_FAR_WATERED_AREA}.geometry, {_NEAR_WATERED_AREA}.geometry)) as geometry,
	0 as {FID},
	{_FAR_WATERED_AREA}.{PADDOCK},
    {_FAR_WATERED_AREA}."{PADDOCK_NAME}",
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
    {_FAR_WATERED_AREA}."{PADDOCK_NAME}",
 	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	{_FAR_WATERED_AREA}.{TIMEFRAME}
from "{_FILTERED_PADDOCKS}"
inner join {_FAR_WATERED_AREA}
	on "{_FILTERED_PADDOCKS}".{FID} = {_FAR_WATERED_AREA}.{PADDOCK}
	and st_difference("{_FILTERED_PADDOCKS}".geometry, {_FAR_WATERED_AREA}.geometry) is not null
	and st_area(st_difference("{_FILTERED_PADDOCKS}".geometry, {_FAR_WATERED_AREA}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	and {Timeframe.timeframesMatchStatuses(f'"{_FAR_WATERED_AREA}"."{TIMEFRAME}"', f'"{_FILTERED_PADDOCKS}"."{STATUS}"')}
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
