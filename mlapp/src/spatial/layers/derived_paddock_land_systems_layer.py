# -*- coding: utf-8 -*-
from ...utils import randomString
from ..calculator import Calculator
from ..features.paddock_land_system import PaddockLandSystem
from ..schemas.schemas import AREA, ESTIMATED_CAPACITY_PER_AREA, CONDITION_DISCOUNT, CONDITION_TYPE, ESTIMATED_CAPACITY, FID, LAND_SYSTEM, LAND_SYSTEM_NAME, NAME, PADDOCK, PADDOCK_NAME, PADDOCK_STATUS, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, WATERED_DISCOUNT, WATERED_TYPE, WATERED_AREA_STATUS
from .derived_feature_layer import DerivedFeatureLayer


class DerivedPaddockLandSystemsLayer(DerivedFeatureLayer):

    STYLE = "paddock_land_systems_popup"

    def parameteriseQuery(self):
        paddockConditionTempView = f"PaddockCondition{randomString()}"

        return f"""
with {paddockConditionTempView} as
	(select
	st_intersection("{{1}}".geometry, "{{2}}".geometry) as geometry,
	"{{0}}".{FID} as {PADDOCK},
	"{{0}}".{NAME} as "{PADDOCK_NAME}",
	"{{0}}".{STATUS} as "{PADDOCK_STATUS}",
	"{{1}}".{FID} as "{LAND_SYSTEM}",
	"{{1}}".{NAME} as "{LAND_SYSTEM_NAME}",
	"{{1}}"."{ESTIMATED_CAPACITY_PER_AREA}" as "{ESTIMATED_CAPACITY_PER_AREA}",
	"{{2}}"."{WATERED_TYPE}",
	"{{2}}".{STATUS} as "{WATERED_AREA_STATUS}"
	from "{{1}}"
	inner join "{{2}}"
		on st_intersects("{{1}}".geometry, "{{2}}".geometry)
		and st_area(st_intersection("{{1}}".geometry, "{{2}}".geometry)) >= {Calculator.MINIMUM_AREA_M2}
	inner join "{{0}}"
		on "{{0}}".{FID} = "{{2}}".{PADDOCK}
		)
select
	st_multi(st_collectionextract(st_union(geometry), 3)) as geometry,
	0 as {FID},
	sum("{AREA}") as "{AREA}",
	(sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	(sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	((sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{ESTIMATED_CAPACITY}",
	((sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{POTENTIAL_CAPACITY}",
	"{CONDITION_TYPE}" as "{CONDITION_TYPE}",
	{PADDOCK} as {PADDOCK},
	"{PADDOCK_NAME}" as "{PADDOCK_NAME}",
	"{PADDOCK_STATUS}" as "{PADDOCK_STATUS}",
	"{LAND_SYSTEM}" as "{LAND_SYSTEM}",
	"{LAND_SYSTEM_NAME}" as "{LAND_SYSTEM_NAME}",
	"{WATERED_AREA_STATUS}" as "{WATERED_AREA_STATUS}"
from
	(select
		0 as {FID},
		{paddockConditionTempView}.geometry,
		{paddockConditionTempView}.{PADDOCK},
		{paddockConditionTempView}."{PADDOCK_NAME}",
		{paddockConditionTempView}."{PADDOCK_STATUS}",
		{paddockConditionTempView}."{LAND_SYSTEM}",
		"{LAND_SYSTEM_NAME}",
		"{ESTIMATED_CAPACITY_PER_AREA}" as "{POTENTIAL_CAPACITY_PER_AREA}",
		st_area({paddockConditionTempView}.geometry) / 1000000 as "{AREA}",
		ifnull("{{3}}"."{CONDITION_TYPE}", 'A') as "{CONDITION_TYPE}",
		case ifnull("{{3}}"."{CONDITION_TYPE}", 'A')
			when 'A' then 1.0
			when 'B' then 0.75
			when 'C' then 0.45
			when 'D' then 0.20
			else 0.0
		end as "{CONDITION_DISCOUNT}",
		{paddockConditionTempView}."{WATERED_TYPE}",
		case {paddockConditionTempView}."{WATERED_TYPE}"
			when 'Near' then 1.0
			when 'Far' then 0.5
			when 'Unwatered' then 0.0
			else 0.0
		end as "{WATERED_DISCOUNT}",
		"{WATERED_AREA_STATUS}"
	 from {paddockConditionTempView}
	 left outer join "{{3}}"
	 	on {paddockConditionTempView}.{PADDOCK} = "{{3}}"."{PADDOCK}"
	 	and {paddockConditionTempView}."{LAND_SYSTEM}" = "{{3}}"."{LAND_SYSTEM}")
where geometry is not null
group by "{PADDOCK}", "{LAND_SYSTEM}", "{CONDITION_TYPE}", "{WATERED_AREA_STATUS}"
"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return PaddockLandSystem

    def __init__(self, project, layerName, paddockLayer, landSystemLayer, wateredAreaLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = self.parameteriseQuery()

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