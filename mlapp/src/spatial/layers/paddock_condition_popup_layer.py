# -*- coding: utf-8 -*-
from ...utils import randomString
from ..calculator import Calculator
from ..features.condition import Condition
from ..schemas.schemas import AREA, CAPACITY_PER_AREA, CONDITION_TYPE, ESTIMATED_CAPACITY, FID, LAND_SYSTEM, LAND_SYSTEM_NAME, NAME, PADDOCK, PADDOCK_NAME, PADDOCK_STATUS, POTENTIAL_CAPACITY, STATUS, WATERED_TYPE, WATERED_AREA_STATUS
from .derived_feature_layer import DerivedFeatureLayer


class PaddockConditionPopupLayer(DerivedFeatureLayer):

    STYLE = "paddock_condition_popup"

    def parameteriseQuery(self, paddockId, paddockName, paddockStatus):
        paddockConditionTempView = f"PaddockCondition{randomString()}"

        return f"""
with {paddockConditionTempView} as
	(select
	st_intersection("{{1}}".geometry, "{{2}}".geometry) as geometry,
	"{{1}}".{FID} as "{LAND_SYSTEM}",
	"{{1}}".{NAME} as "{LAND_SYSTEM_NAME}",
	"{{1}}"."{CAPACITY_PER_AREA}" as "{CAPACITY_PER_AREA}",
	"{{2}}"."{WATERED_TYPE}",
	"{{2}}".{STATUS} as "{WATERED_AREA_STATUS}"
	from "{{1}}"
	inner join "{{2}}"
		on "{{2}}".{PADDOCK} = {paddockId}
		and st_intersects("{{1}}".geometry, "{{2}}".geometry)
		and st_area(st_intersection("{{1}}".geometry, "{{2}}".geometry)) >= {Calculator.MINIMUM_AREA_M2})
select
	geometry,
	row_number() over (order by '') as {FID},
	{paddockId} as {PADDOCK},
	'{paddockName}' as "{PADDOCK_NAME}",
	'{paddockStatus}' as "{PADDOCK_STATUS}",
	"{LAND_SYSTEM}",
	"{LAND_SYSTEM_NAME}",
	"{CAPACITY_PER_AREA}",
	"{AREA}",
	("{CAPACITY_PER_AREA}" * "{AREA}") as "{ESTIMATED_CAPACITY}",
	("{CAPACITY_PER_AREA}" * "{AREA}") as "{POTENTIAL_CAPACITY}",
	"{CONDITION_TYPE}",
	"{WATERED_TYPE}",
	"{WATERED_AREA_STATUS}"
from
	(select
		{paddockConditionTempView}.geometry,
		{paddockConditionTempView}."{LAND_SYSTEM}",
		"{LAND_SYSTEM_NAME}",
		"{CAPACITY_PER_AREA}",
		st_area({paddockConditionTempView}.geometry) / 1000000 as "{AREA}",
		ifnull("{{3}}"."{CONDITION_TYPE}", 'A') as "{CONDITION_TYPE}",
		{paddockConditionTempView}."{WATERED_TYPE}",
		"{WATERED_AREA_STATUS}"
	 from
	 {paddockConditionTempView} left outer join "{{3}}"
	 on {paddockId} = "{{3}}"."{PADDOCK}"
	 and {paddockConditionTempView}."{LAND_SYSTEM}" = "{{3}}"."{LAND_SYSTEM}"
	 and {paddockConditionTempView}."{WATERED_TYPE}" = "{{3}}"."{WATERED_TYPE}")
where geometry is not null
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return Condition

    def __init__(self, layerName, paddock, paddockLayer, landSystemLayer, wateredAreaLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = self.parameteriseQuery(paddockId=paddock.id,
                                       paddockName=paddock.name,
                                       paddockStatus=paddock.status)

        super().__init__(
            layerName,
            query,
            PaddockConditionPopupLayer.STYLE,
            paddockLayer,
            landSystemLayer,
            wateredAreaLayer,
            conditionTable)

        self.conditionTable = conditionTable

    def wrapFeature(self, feature):
        return Condition(self, self.conditionTable, feature)
