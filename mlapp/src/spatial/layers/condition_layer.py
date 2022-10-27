# -*- coding: utf-8 -*-
from ..features.condition import Condition
from .derived_layer import DerivedLayer


class ConditionLayer(DerivedLayer):

    ALTERNATIVE_QUERY = """
with "Paddock Condition" as
(with
"Paddock Land Systems" as
(select
 st_intersection("{0}".geometry, "{1}".geometry) as "geometry",
 "{0}".fid as "Paddock",
 "{0}"."Name" as "Paddock Name",
 "{0}"."Status" as "Paddock Status",
 "{1}".fid as "Land System",
 "{1}"."Name" as "Land System Name",
 "{1}"."AE/km²" as "AE/km²",
 'A' as "Condition"
from "{0}"
inner join "{1}"
on st_intersects("{0}".geometry, "{1}".geometry)),
"Watered Areas" as
(select
 st_union(geometry) as "geometry",
 "Waterpoint Buffer Type",
 "Status"
 from "{2}"
 group by "Waterpoint Buffer Type", "Status")
select
st_intersection("Paddock Land Systems".geometry, "Watered Areas".geometry) as "geometry",
"Paddock",
"Paddock Name",
"Paddock Status",
"Land System",
"Land System Name",
"AE/km²" as "AE/km²",
"Condition",
"Waterpoint Buffer Type",
"Watered Areas"."Status" as "Watered Area Status"
from "Paddock Land Systems"
inner join "Watered Areas"
on st_intersects("Watered Areas".geometry, "Paddock Land Systems".geometry))
select
"Paddock Condition".geometry,
"Paddock Condition"."Paddock",
"Paddock Name",
"Paddock Status",
"Paddock Condition"."Land System",
"Land System Name",
"AE/km²" as "AE/km²",
ifnull("{3}"."Condition", 'A') as "Condition",
"Paddock Condition"."Waterpoint Buffer Type",
"Watered Area Status"
from
"Paddock Condition" left outer join "{3}"
on "Paddock Condition"."Paddock" = "{3}"."Paddock"
and "Paddock Condition"."Land System" = "{3}"."Land System"
and "Paddock Condition"."Waterpoint Buffer Type" = "{3}"."Waterpoint Buffer Type"

"""

    QUERY = """
with
"Paddock Land Systems" as
(select
 st_intersection("{0}".geometry, "{1}".geometry) as "geometry",
 "{0}".fid as "Paddock",
 "{0}"."Name" as "Paddock Name",
 "{0}"."Status" as "Paddock Status",
 "{1}".fid as "Land System",
 "{1}"."Name" as "Land System Name",
 "{1}"."AE/km²" as "AE/km²",
 'A' as "Condition"
from "{0}"
inner join "{1}"
on st_intersects("{0}".geometry, "{1}".geometry)),
"Watered Areas" as
(select
 st_union(geometry) as "geometry",
 "Waterpoint Buffer Type",
 "Status"
 from "{2}"
 group by "Waterpoint Buffer Type", "Status")
select
st_intersection("Paddock Land Systems".geometry, "Watered Areas".geometry) as "geometry",
"Paddock",
"Paddock Name",
"Paddock Status",
"Land System",
"Land System Name",
"AE/km²" as "AE/km²",
"Condition",
"Waterpoint Buffer Type",
"Watered Areas"."Status" as "Watered Area Status"
from "Paddock Land Systems"
inner join "Watered Areas"
on st_intersects("Watered Areas".geometry, "Paddock Land Systems".geometry)

"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return Condition

    def __init__(self, layerName, paddockLayer, landSystemLayer, waterpointBufferLayer, conditionTable):
        super().__init__(
            layerName,
            ConditionLayer.ALTERNATIVE_QUERY,
            None,
            paddockLayer,
            landSystemLayer,
            waterpointBufferLayer,
            conditionTable)
