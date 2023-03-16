# -*- coding: utf-8 -*-
from ..utils import randomString
from .calculator import Calculator
from .derived_feature_layer import DerivedFeatureLayer
from .features import PaddockLandType
from .fields import AREA, ESTIMATED_CAPACITY_PER_AREA, CONDITION_DISCOUNT, CONDITION_TYPE, ESTIMATED_CAPACITY, FID, LAND_TYPE, LAND_TYPE_NAME, NAME, OPTIMAL_CAPACITY_PER_AREA, PADDOCK, PADDOCK_NAME, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, TIMEFRAME, WATERED_DISCOUNT, WATERED_TYPE, WATERED_AREA, Timeframe


class DerivedPaddockLandTypesLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Paddock Land Types"
    STYLE = "paddock_land_types_popup"

    @classmethod
    def getFeatureType(cls):
        return PaddockLandType

    def getRederiveFeaturesRequest(self):
        """Define which features must be removed from a target layer to be re-derived."""
        if not self.changeset:
            return None

        # TODO Land Type condition table?
        [landTypeConditionTable, basePaddockLayer, landTypeLayer, wateredAreaLayer] = self.dependentLayers
        return self.prepareRederiveFeaturesRequest(
            basePaddockLayer, PADDOCK, FID,
            wateredAreaLayer, PADDOCK, PADDOCK,
            landTypeLayer, LAND_TYPE, FID)

    def prepareQuery(self, query, dependentLayers):
        [landTypeConditionTable, basePaddockLayer, landTypeLayer, wateredAreaLayer] = dependentLayers
        [landTypeConditions, basePaddocks, landTypes, wateredAreas] = self.names(dependentLayers)

        _PADDOCK_LAND_TYPES = f"PaddockLandTypes{randomString()}"
        _PADDOCK_WATERED_AREAS = f"PaddockWateredAreas{randomString()}"
        _WATERED_FACTOR = "WateredFactor"

        filterPaddocks = self.andAllKeyClauses(self.changeset, basePaddockLayer,
                                               FID, FID, wateredAreaLayer, FID, PADDOCK)

        if filterPaddocks:
            _FILTERED_PADDOCKS = f"FilteredPaddocks{randomString()}"
            withFilteredPaddocks = f"""
  {_FILTERED_PADDOCKS} as
    (select * from "{basePaddocks}"
     where 1=1
     {filterPaddocks}),
"""
        else:
            _FILTERED_PADDOCKS = basePaddocks
            withFilteredPaddocks = ""

        query = f"""
with
 {withFilteredPaddocks}
 {_PADDOCK_WATERED_AREAS} as
	(select
		"{wateredAreas}".geometry as geometry,
		"{_FILTERED_PADDOCKS}".{FID} as {PADDOCK},
		"{_FILTERED_PADDOCKS}".{NAME},
		"{wateredAreas}"."{WATERED_TYPE}",
		"{wateredAreas}".{TIMEFRAME}
	from "{_FILTERED_PADDOCKS}"
	inner join "{wateredAreas}"
		on "{_FILTERED_PADDOCKS}".{FID} = "{wateredAreas}".{PADDOCK}
		and {Timeframe.timeframesIncludeStatuses(f'"{wateredAreas}".{TIMEFRAME}', f'"{_FILTERED_PADDOCKS}".{STATUS}')}
	)
, {_PADDOCK_LAND_TYPES} as
	(select
		st_intersection("{landTypes}".geometry, {_PADDOCK_WATERED_AREAS}.geometry) as geometry,
		{_PADDOCK_WATERED_AREAS}.{PADDOCK},
		{_PADDOCK_WATERED_AREAS}.{NAME} as "{PADDOCK_NAME}",
		{_PADDOCK_WATERED_AREAS}."{WATERED_TYPE}",
		{_PADDOCK_WATERED_AREAS}.{TIMEFRAME},
		"{landTypes}".{FID} as "{LAND_TYPE}",
		"{landTypes}"."{LAND_TYPE_NAME}" as "{LAND_TYPE_NAME}",
		"{landTypes}"."{OPTIMAL_CAPACITY_PER_AREA}" as "{ESTIMATED_CAPACITY_PER_AREA}"
	from "{landTypes}"
	inner join {_PADDOCK_WATERED_AREAS}
		on st_intersects("{landTypes}".geometry, {_PADDOCK_WATERED_AREAS}.geometry)
		and st_area(st_intersection("{landTypes}".geometry, {_PADDOCK_WATERED_AREAS}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	)
select
	st_multi(st_collectionextract(st_union(geometry), 3)) as geometry,
	0 as {FID},
 	{PADDOCK},
  	"{LAND_TYPE}",
   	"{PADDOCK_NAME}",
	"{LAND_TYPE_NAME}",
 	"{CONDITION_TYPE}",
	{TIMEFRAME} as {TIMEFRAME},
	sum("{AREA}") as "{AREA}",
	sum("{AREA}" * "{_WATERED_FACTOR}") as "{WATERED_AREA}",
	(sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	(sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	((sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{ESTIMATED_CAPACITY}",
	((sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{POTENTIAL_CAPACITY}"
from
	(select
		0 as {FID},
		{_PADDOCK_LAND_TYPES}.geometry,
		{_PADDOCK_LAND_TYPES}.{PADDOCK},
		{_PADDOCK_LAND_TYPES}."{PADDOCK_NAME}",
		{_PADDOCK_LAND_TYPES}."{LAND_TYPE}",
		"{LAND_TYPE_NAME}",
		"{ESTIMATED_CAPACITY_PER_AREA}" as "{POTENTIAL_CAPACITY_PER_AREA}",
		st_area({_PADDOCK_LAND_TYPES}.geometry) / 1000000 as "{AREA}",
		case {_PADDOCK_LAND_TYPES}."{WATERED_TYPE}"
			when 'Near' then 1.0
			when 'Far' then 1.0
			when 'Unwatered' then 0.0
			else 0.0
		end as {_WATERED_FACTOR},
        ifnull("{landTypeConditions}"."{CONDITION_TYPE}", 'A') as "{CONDITION_TYPE}",
		case ifnull("{landTypeConditions}"."{CONDITION_TYPE}", 'A')
			when 'A' then 1.0
			when 'B' then 0.75
			when 'C' then 0.45
			when 'D' then 0.20
			else 0.0
		end as "{CONDITION_DISCOUNT}",
		{_PADDOCK_LAND_TYPES}."{WATERED_TYPE}",
		case {_PADDOCK_LAND_TYPES}."{WATERED_TYPE}"
			when 'Near' then 1.0
			when 'Far' then 0.5
			when 'Unwatered' then 0.0
			else 0.0
		end as "{WATERED_DISCOUNT}",
		{TIMEFRAME}
	 from {_PADDOCK_LAND_TYPES}
	 left outer join "{landTypeConditions}"
	 	on {_PADDOCK_LAND_TYPES}.{PADDOCK} = "{landTypeConditions}"."{PADDOCK}"
	 	and {_PADDOCK_LAND_TYPES}."{LAND_TYPE}" = "{landTypeConditions}"."{LAND_TYPE}")
where geometry is not null
group by "{PADDOCK}", "{LAND_TYPE}", "{CONDITION_TYPE}", {TIMEFRAME}
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(DerivedPaddockLandTypesLayer.defaultName(),
                         DerivedPaddockLandTypesLayer.defaultStyle(),
                         dependentLayers,
                         changeset)
