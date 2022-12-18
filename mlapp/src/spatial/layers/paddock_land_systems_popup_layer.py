# -*- coding: utf-8 -*-
from ...utils import randomString
from ..calculator import Calculator
from ..features.paddock_land_system import PaddockLandSystem
from ..schemas.schemas import AREA, ESTIMATED_CAPACITY_PER_AREA, CONDITION_DISCOUNT, CONDITION_TYPE, ESTIMATED_CAPACITY, FID, LAND_SYSTEM, LAND_SYSTEM_NAME, NAME, PADDOCK, PADDOCK_NAME, PADDOCK_STATUS, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, WATERED_DISCOUNT, WATERED_TYPE, WATERED_AREA_STATUS
from .derived_feature_layer import DerivedFeatureLayer


class PaddockLandSystemsPopupLayer(DerivedFeatureLayer):

    STYLE = "paddock_land_systems_popup"

    def parameteriseQuery(self, paddockId, paddockName, paddockStatus):
        paddockConditionTempView = f"PaddockCondition{randomString()}"

        return f"""
with {paddockConditionTempView} as
	(select
	st_intersection("{{1}}".geometry, "{{2}}".geometry) as geometry,
	"{{1}}".{FID} as "{LAND_SYSTEM}",
	"{{1}}".{NAME} as "{LAND_SYSTEM_NAME}",
	"{{1}}"."{ESTIMATED_CAPACITY_PER_AREA}" as "{ESTIMATED_CAPACITY_PER_AREA}",
	"{{2}}"."{WATERED_TYPE}",
	"{{2}}".{STATUS} as "{WATERED_AREA_STATUS}"
	from "{{1}}"
	inner join "{{2}}"
		on "{{2}}".{PADDOCK} = {paddockId}
		and st_intersects("{{1}}".geometry, "{{2}}".geometry)
		and st_area(st_intersection("{{1}}".geometry, "{{2}}".geometry)) >= {Calculator.MINIMUM_AREA_M2})
select
	st_multi(st_union(geometry)) as geometry,
	row_number() over (order by '') as {FID},
	{paddockId} as {PADDOCK},
	'{paddockName}' as "{PADDOCK_NAME}",
	'{paddockStatus}' as "{PADDOCK_STATUS}",
	"{LAND_SYSTEM}",
	"{LAND_SYSTEM_NAME}",
	(sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	(sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	sum("{AREA}") as "{AREA}",
	((sum("{AREA}" * ("{POTENTIAL_CAPACITY_PER_AREA}" * "{CONDITION_DISCOUNT}" * "{WATERED_DISCOUNT}")) / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{ESTIMATED_CAPACITY}",
	((sum("{AREA}" * "{POTENTIAL_CAPACITY_PER_AREA}") / nullif(sum("{AREA}"), 0.0)) * "{AREA}") as "{POTENTIAL_CAPACITY}",
	"{CONDITION_TYPE}",
	"{WATERED_AREA_STATUS}"
from
	(select
		{paddockConditionTempView}.geometry,
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
	 	on {paddockId} = "{{3}}"."{PADDOCK}"
	 	and {paddockConditionTempView}."{LAND_SYSTEM}" = "{{3}}"."{LAND_SYSTEM}")
where geometry is not null
group by "{LAND_SYSTEM}", "{CONDITION_TYPE}", "{WATERED_AREA_STATUS}"
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return PaddockLandSystem

    def __init__(self, project, layerName, paddock, paddockLayer, landSystemLayer, wateredAreaLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = self.parameteriseQuery(paddockId=paddock.id,
                                       paddockName=paddock.name,
                                       paddockStatus=paddock.status)

        super().__init__(
            project,
            layerName,
            query,
            PaddockLandSystemsPopupLayer.STYLE,
            paddockLayer,
            landSystemLayer,
            wateredAreaLayer,
            conditionTable)

        self.conditionTable = conditionTable

    def wrapFeature(self, feature):
        return PaddockLandSystem(self, self.conditionTable, feature)
