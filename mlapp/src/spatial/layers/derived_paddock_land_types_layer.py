# -*- coding: utf-8 -*-
from ...utils import randomString
from ..calculator import Calculator
from ..features.paddock_land_type import PaddockLandType
from ..fields.names import AREA, ESTIMATED_CAPACITY_PER_AREA, CONDITION_DISCOUNT, CONDITION_TYPE, ESTIMATED_CAPACITY, FID, LAND_TYPE, LAND_TYPE_NAME, NAME, OPTIMAL_CAPACITY_PER_AREA, PADDOCK, PADDOCK_NAME, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, TIMEFRAME, WATERED_DISCOUNT, WATERED_TYPE, WATERED_AREA
from ..fields.timeframe import Timeframe
from .derived_feature_layer import DerivedFeatureLayer


class DerivedPaddockLandTypesLayer(DerivedFeatureLayer):

    STYLE = "paddock_land_types_popup"

    def parameteriseQuery(self, PaddockLayer, LandTypeLayer, WateredAreaLayer, ConditionTable):
        PaddockLandTypes = f"PaddockLandTypes{randomString()}"
        PaddockWateredAreas = f"PaddockWateredAreas{randomString()}"
        WateredFactor = "WateredFactor"

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
{PaddockLandTypes} as
	(select
		st_intersection("{LandTypeLayer}".geometry, {PaddockWateredAreas}.geometry) as geometry,
		{PaddockWateredAreas}.{PADDOCK},
		{PaddockWateredAreas}.{NAME} as "{PADDOCK_NAME}",
		{PaddockWateredAreas}."{WATERED_TYPE}",
		{PaddockWateredAreas}.{TIMEFRAME},
		"{LandTypeLayer}".{FID} as "{LAND_TYPE}",
		"{LandTypeLayer}".{NAME} as "{LAND_TYPE_NAME}",
		"{LandTypeLayer}"."{OPTIMAL_CAPACITY_PER_AREA}" as "{ESTIMATED_CAPACITY_PER_AREA}"
	from "{LandTypeLayer}"
	inner join {PaddockWateredAreas}
		on st_intersects("{LandTypeLayer}".geometry, {PaddockWateredAreas}.geometry)
		and st_area(st_intersection("{LandTypeLayer}".geometry, {PaddockWateredAreas}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	)
select
	st_multi(st_collectionextract(st_union(geometry), 3)) as geometry,
	0 as {FID},
	sum("{AREA}") as "{AREA}",
	sum("{AREA}" * "{WateredFactor}") as "{WATERED_AREA}",
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
		{PaddockLandTypes}.geometry,
		{PaddockLandTypes}.{PADDOCK},
		{PaddockLandTypes}."{PADDOCK_NAME}",
		{PaddockLandTypes}."{LAND_TYPE}",
		"{LAND_TYPE_NAME}",
		"{ESTIMATED_CAPACITY_PER_AREA}" as "{POTENTIAL_CAPACITY_PER_AREA}",
		st_area({PaddockLandTypes}.geometry) / 1000000 as "{AREA}",
		case {PaddockLandTypes}."{WATERED_TYPE}"
			when 'Near' then 1.0
			when 'Far' then 1.0
			when 'Unwatered' then 0.0
			else 0.0
		end as {WateredFactor},
        ifnull("{ConditionTable}"."{CONDITION_TYPE}", 'A') as "{CONDITION_TYPE}",
		case ifnull("{ConditionTable}"."{CONDITION_TYPE}", 'A')
			when 'A' then 1.0
			when 'B' then 0.75
			when 'C' then 0.45
			when 'D' then 0.20
			else 0.0
		end as "{CONDITION_DISCOUNT}",
		{PaddockLandTypes}."{WATERED_TYPE}",
		case {PaddockLandTypes}."{WATERED_TYPE}"
			when 'Near' then 1.0
			when 'Far' then 0.5
			when 'Unwatered' then 0.0
			else 0.0
		end as "{WATERED_DISCOUNT}",
		{TIMEFRAME}
	 from {PaddockLandTypes}
	 left outer join "{ConditionTable}"
	 	on {PaddockLandTypes}.{PADDOCK} = "{ConditionTable}"."{PADDOCK}"
	 	and {PaddockLandTypes}."{LAND_TYPE}" = "{ConditionTable}"."{LAND_TYPE}")
where geometry is not null
group by "{PADDOCK}", "{LAND_TYPE}", "{CONDITION_TYPE}", {TIMEFRAME}
"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return PaddockLandType

    def __init__(self, project, layerName, paddockLayer, landTypeLayer, wateredAreaLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = self.parameteriseQuery(
            paddockLayer.name(),
            landTypeLayer.name(),
            wateredAreaLayer.name(),
            conditionTable.name())

        super().__init__(
            project,
            layerName,
            query,
            DerivedPaddockLandTypesLayer.STYLE,
            paddockLayer,
            landTypeLayer,
            wateredAreaLayer,
            conditionTable)

        self.conditionTable = conditionTable

    def wrapFeature(self, feature):
        # Burn in the FID that gets generated by QGIS for consistency
        feature.setAttribute(FID, feature.id())
        return PaddockLandType(self, self.conditionTable, feature)
