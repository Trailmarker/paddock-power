# -*- coding: utf-8 -*-
from ...utils import randomString
from ..calculator import Calculator
from ..features.paddock_land_system import PaddockLandSystem
from ..fields.schemas import AREA, ESTIMATED_CAPACITY_PER_AREA, CONDITION_DISCOUNT, CONDITION_TYPE, ESTIMATED_CAPACITY, FID, LAND_SYSTEM, LAND_SYSTEM_NAME, NAME, OPTIMAL_CAPACITY_PER_AREA, PADDOCK, PADDOCK_NAME, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, TIMEFRAME, WATERED_DISCOUNT, WATERED_TYPE, WATERED_AREA_STATUS
from ..fields.timeframe import Timeframe
from .derived_feature_layer import DerivedFeatureLayer


class DerivedPaddockLandSystemsLayer(DerivedFeatureLayer):

    STYLE = "paddock_land_systems_popup"

    def parameteriseQuery(self, PaddockLayer, LandSystemLayer, WateredAreaLayer, ConditionTable):
        PaddockLandSystems = f"PaddockLandSystems{randomString()}"
        PaddockWateredAreas = f"PaddockWateredAreas{randomString()}"

        return f"""
with {PaddockWateredAreas} as
	(select
		"{WateredAreaLayer}".geometry as geometry,
		"{PaddockLayer}".{FID} as {PADDOCK},
		"{PaddockLayer}".{NAME},
		"{WateredAreaLayer}"."{WATERED_TYPE}",
		"{WateredAreaLayer}".{TIMEFRAME}
	from "{PaddockLayer}"
	inner join "{WateredAreaLayer}"
		on "{PaddockLayer}".{FID} = "{WateredAreaLayer}".{PADDOCK}
		and {Timeframe.timeframesIncludeStatuses(f'"{WateredAreaLayer}".{TIMEFRAME}', f'"{PaddockLayer}".{STATUS}')}
	),
{PaddockLandSystems} as
	(select
		st_intersection("{LandSystemLayer}".geometry, {PaddockWateredAreas}.geometry) as geometry,
		{PaddockWateredAreas}.{PADDOCK},
		{PaddockWateredAreas}.{NAME} as "{PADDOCK_NAME}",
		{PaddockWateredAreas}."{WATERED_TYPE}",
		{PaddockWateredAreas}.{TIMEFRAME},
		"{LandSystemLayer}".{FID} as "{LAND_SYSTEM}",
		"{LandSystemLayer}".{NAME} as "{LAND_SYSTEM_NAME}",
		"{LandSystemLayer}"."{OPTIMAL_CAPACITY_PER_AREA}" as "{ESTIMATED_CAPACITY_PER_AREA}"
	from "{LandSystemLayer}"
	inner join {PaddockWateredAreas}
		on st_intersects("{LandSystemLayer}".geometry, {PaddockWateredAreas}.geometry)
		and st_area(st_intersection("{LandSystemLayer}".geometry, {PaddockWateredAreas}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	)
select
	st_multi(st_collectionextract(st_union(geometry), 3)) as geometry,
	0 as {FID},
	sum("{AREA}") as "{AREA}",
	(sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	(sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	((sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{ESTIMATED_CAPACITY}",
	((sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{POTENTIAL_CAPACITY}",
	"{CONDITION_TYPE}",
	{PADDOCK},
	"{PADDOCK_NAME}",
	"{LAND_SYSTEM}",
	"{LAND_SYSTEM_NAME}",
	{TIMEFRAME} as {TIMEFRAME}
from
	(select
		0 as {FID},
		{PaddockLandSystems}.geometry,
		{PaddockLandSystems}.{PADDOCK},
		{PaddockLandSystems}."{PADDOCK_NAME}",
		{PaddockLandSystems}."{LAND_SYSTEM}",
		"{LAND_SYSTEM_NAME}",
		"{ESTIMATED_CAPACITY_PER_AREA}" as "{POTENTIAL_CAPACITY_PER_AREA}",
		st_area({PaddockLandSystems}.geometry) / 1000000 as "{AREA}",
		ifnull("{ConditionTable}"."{CONDITION_TYPE}", 'A') as "{CONDITION_TYPE}",
		case ifnull("{ConditionTable}"."{CONDITION_TYPE}", 'A')
			when 'A' then 1.0
			when 'B' then 0.75
			when 'C' then 0.45
			when 'D' then 0.20
			else 0.0
		end as "{CONDITION_DISCOUNT}",
		{PaddockLandSystems}."{WATERED_TYPE}",
		case {PaddockLandSystems}."{WATERED_TYPE}"
			when 'Near' then 1.0
			when 'Far' then 0.5
			when 'Unwatered' then 0.0
			else 0.0
		end as "{WATERED_DISCOUNT}",
		{TIMEFRAME}
	 from {PaddockLandSystems}
	 left outer join "{ConditionTable}"
	 	on {PaddockLandSystems}.{PADDOCK} = "{ConditionTable}"."{PADDOCK}"
	 	and {PaddockLandSystems}."{LAND_SYSTEM}" = "{ConditionTable}"."{LAND_SYSTEM}")
where geometry is not null
group by "{PADDOCK}", "{LAND_SYSTEM}", "{CONDITION_TYPE}", {TIMEFRAME}
"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return PaddockLandSystem

    def __init__(self, project, layerName, paddockLayer, landSystemLayer, wateredAreaLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = self.parameteriseQuery(paddockLayer.name(), landSystemLayer.name(), wateredAreaLayer.name(), conditionTable.name())

        super().__init__(
            project,
            layerName,
            query,
            DerivedPaddockLandSystemsLayer.STYLE,
            paddockLayer,
            landSystemLayer,
            wateredAreaLayer,
            conditionTable)

        self.conditionTable = conditionTable

    def wrapFeature(self, feature):
        # Burn in the FID that gets generated by QGIS for consistency
        feature.setAttribute(FID, feature.id())
        return PaddockLandSystem(self, self.conditionTable, feature)
