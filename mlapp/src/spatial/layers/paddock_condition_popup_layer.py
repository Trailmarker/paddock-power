# -*- coding: utf-8 -*-
from ..features.condition import Condition
from .derived_layer import DerivedLayer


class PaddockConditionPopupLayer(DerivedLayer):

    STYLE = "paddock_condition_popup"

    QUERY = """
with "Paddock Condition" as
	(with "Paddock" as
		(select geometry from "{{0}}" where fid = {paddockId})
	select
	st_intersection(st_intersection("Paddock".geometry, "{{1}}".geometry), "{{2}}".geometry) as "geometry",
	"{{1}}".fid as "Land System",
	"{{1}}"."Name" as "Land System Name",
	"AE/km²" as "AE/km²",
	"Watered",
	"{{2}}"."Status" as "Watered Area Status"
	from "Paddock"
	inner join "{{1}}"
	on st_intersects("Paddock".geometry, "{{1}}".geometry)
	inner join "{{2}}"
	on st_intersects("{{1}}".geometry, "{{2}}".geometry))
select
geometry,
row_number() over (order by '') as "fid",
{paddockId} as "Paddock",
'{paddockName}' as "Paddock Name",
'{paddockStatus}' as "Paddock Status",
"Land System",
"Land System Name",
"AE/km²",
"Area (km²)",
("AE/km²" * "Area (km²)") as "AE",
("AE/km²" * "Area (km²)") as "Potential AE",
"Condition",
"Watered",
"Watered Area Status"
from
	(select
	 "Paddock Condition".geometry,
	 "Paddock Condition"."Land System",
	 "Land System Name",
	 "AE/km²",
 	 st_area("Paddock Condition".geometry) / 1000000 as "Area (km²)",
 	 ifnull("{{3}}"."Condition", 'A') as "Condition",
	 "Paddock Condition"."Watered",
	 "Watered Area Status"
	 from
	 "Paddock Condition" left outer join "{{3}}"
	 on {paddockId} = "{{3}}"."Paddock"
	 and "Paddock Condition"."Land System" = "{{3}}"."Land System"
	 and "Paddock Condition"."Watered" = "{{3}}"."Watered")
where geometry is not null
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return Condition

    def __init__(self, layerName, paddock, paddockLayer, landSystemLayer, wateredAreaLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = PaddockConditionPopupLayer.QUERY.format(paddockId=paddock.id,
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
