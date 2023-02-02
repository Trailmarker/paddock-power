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

    def prepareQuery(self, query, *dependentLayers):

        [conditionTable, paddockLayer, landTypeLayer, wateredAreaLayer] = self.names(*dependentLayers)

        _PADDOCK_LAND_TYPES = f"PaddockLandTypes{randomString()}"
        _PADDOCK_WATERED_AREAS = f"PaddockWateredAreas{randomString()}"
        _WATERED_FACTOR = "WateredFactor"

        query = f"""
with {_PADDOCK_WATERED_AREAS} as
	(select
		"{wateredAreaLayer}".geometry as geometry,
		"{paddockLayer}".{FID} as {PADDOCK},
		"{paddockLayer}".{NAME},
		"{wateredAreaLayer}"."{WATERED_TYPE}",
		"{wateredAreaLayer}".{TIMEFRAME}
	from "{paddockLayer}"
	inner join "{wateredAreaLayer}"
		on "{paddockLayer}".{FID} = "{wateredAreaLayer}".{PADDOCK}
		and {Timeframe.timeframesIncludeStatuses(f'"{wateredAreaLayer}".{TIMEFRAME}', f'"{paddockLayer}".{STATUS}')}
	),
{_PADDOCK_LAND_TYPES} as
	(select
		st_intersection("{landTypeLayer}".geometry, {_PADDOCK_WATERED_AREAS}.geometry) as geometry,
		{_PADDOCK_WATERED_AREAS}.{PADDOCK},
		{_PADDOCK_WATERED_AREAS}.{NAME} as "{PADDOCK_NAME}",
		{_PADDOCK_WATERED_AREAS}."{WATERED_TYPE}",
		{_PADDOCK_WATERED_AREAS}.{TIMEFRAME},
		"{landTypeLayer}".{FID} as "{LAND_TYPE}",
		"{landTypeLayer}"."{LAND_TYPE_NAME}" as "{LAND_TYPE_NAME}",
		"{landTypeLayer}"."{OPTIMAL_CAPACITY_PER_AREA}" as "{ESTIMATED_CAPACITY_PER_AREA}"
	from "{landTypeLayer}"
	inner join {_PADDOCK_WATERED_AREAS}
		on st_intersects("{landTypeLayer}".geometry, {_PADDOCK_WATERED_AREAS}.geometry)
		and st_area(st_intersection("{landTypeLayer}".geometry, {_PADDOCK_WATERED_AREAS}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	)
select
	st_multi(st_collectionextract(st_union(geometry), 3)) as geometry,
	0 as {FID},
	sum("{AREA}") as "{AREA}",
	sum("{AREA}" * "{_WATERED_FACTOR}") as "{WATERED_AREA}",
	(sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	(sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	((sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{ESTIMATED_CAPACITY}",
	((sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{POTENTIAL_CAPACITY}",
	"{CONDITION_TYPE}",
	{PADDOCK},
	"{PADDOCK_NAME}",
	"{LAND_TYPE}",
	"{LAND_TYPE_NAME}",
	{TIMEFRAME} as {TIMEFRAME}
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
        ifnull("{conditionTable}"."{CONDITION_TYPE}", 'A') as "{CONDITION_TYPE}",
		case ifnull("{conditionTable}"."{CONDITION_TYPE}", 'A')
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
	 left outer join "{conditionTable}"
	 	on {_PADDOCK_LAND_TYPES}.{PADDOCK} = "{conditionTable}"."{PADDOCK}"
	 	and {_PADDOCK_LAND_TYPES}."{LAND_TYPE}" = "{conditionTable}"."{LAND_TYPE}")
where geometry is not null
group by "{PADDOCK}", "{LAND_TYPE}", "{CONDITION_TYPE}", {TIMEFRAME}
"""
        return super().prepareQuery(query)

    def __init__(self,
                 conditionTable,
                 paddockLayer,
                 landTypeLayer,
                 wateredAraLayer):

        super().__init__(DerivedPaddockLandTypesLayer.defaultName(),
                         DerivedPaddockLandTypesLayer.defaultStyle(),
                         conditionTable,
                         paddockLayer,
                         landTypeLayer,
                         wateredAraLayer)
