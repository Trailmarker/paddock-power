# -*- coding: utf-8 -*-
from ..features.condition import Condition
from .derived_layer import DerivedLayer


class PaddockConditionLayer(DerivedLayer):

    STYLE = "paddock_condition"

# (with 
#   "Watered Areas" as
#     (with
# 		"Near" as
# 			(select
# 			 st_union(geometry) as "geometry",
# 			 "Status"
# 			 from "Waterpoint Buffers"
# 			 where "Waterpoint Buffer Type" = 'Near'
# 			 group by "Status")
# 		, "Far" as
# 			(select
# 			 st_union(geometry) as "geometry",
# 			 "Status"
# 			 from "Waterpoint Buffers"
# 			 where "Waterpoint Buffer Type" = 'Far'
# 			 group by "Status")
# 		, "Farm" as
# 			(select st_union(geometry) as "geometry"
# 			 from
# 			 (select geometry from "Paddocks"
# 			  union
# 			  select geometry from "Waterpoint Buffers"))
# 	 select "geometry", 'Near' as "Watered", "Status" 
# 	 from "Near"
# 	 union
# 	 select st_difference("Far".geometry, "Near".geometry), 'Far' as "Watered", "Far"."Status"
# 	 from "Far"
# 	 inner join "Near"
# 	 on "Far"."Status" = "Near"."Status"
# 	 union
# 	 select st_difference("Farm".geometry, "Far".geometry), 'Unwatered' as "Watered", "Far"."Status"
# 	 from "Farm", "Far")
# , "Paddock" as
# 	 (select geometry from "Paddocks" where fid = 55)


    QUERY = """
with "Paddock Condition" as
(with 
  "Watered Areas" as
    (with
		"Near" as
			(select
			 st_union(geometry) as "geometry",
			 "Status"
			 from "{{2}}"
			 where "Waterpoint Buffer Type" = 'Near'
			 group by "Status")
		, "Far" as
			(select
			 st_union(geometry) as "geometry",
			 "Status"
			 from "{{2}}"
			 where "Waterpoint Buffer Type" = 'Far'
			 group by "Status")
		, "Farm" as
			(select st_union(geometry) as "geometry"
			 from
			 (select geometry from "{{0}}"
			  union
			  select geometry from "{{2}}"))
	 select "geometry", 'Near' as "Watered", "Status" 
	 from "Near"
	 union
	 select st_difference("Far".geometry, "Near".geometry), 'Far' as "Watered", "Far"."Status"
	 from "Far"
	 inner join "Near"
	 on "Far"."Status" = "Near"."Status"
	 union
	 select st_difference("Farm".geometry, "Far".geometry), 'Unwatered' as "Watered", "Far"."Status"
	 from "Farm", "Far"),
  "Paddock" as
	(select geometry from "{{0}}" where fid = {paddockId})
select
st_intersection(st_intersection("Paddock".geometry, "{{1}}".geometry), "Watered Areas".geometry) as "geometry",
"{{1}}".fid as "Land System",
"{{1}}"."Name" as "Land System Name",
"AE/km²" as "AE/km²",
"Watered",
"Watered Areas"."Status" as "Watered Area Status"
from "Paddock"
inner join "{{1}}"
on st_intersects("Paddock".geometry, "{{1}}".geometry)
inner join "Watered Areas"
on st_intersects("{{1}}".geometry, "Watered Areas".geometry))
select
"Paddock Condition".geometry,
{paddockId} as "Paddock",
'{paddockName}' as "Paddock Name",
'{paddockStatus}' as "Paddock Status",
"Paddock Condition"."Land System",
"Land System Name",
"AE/km²",
ifnull("{{3}}"."Condition", 'A') as "Condition",
"Paddock Condition"."Watered",
"Watered Area Status"
from
"Paddock Condition" left outer join "{{3}}"
on {paddockId} = "{{3}}"."Paddock"
and "Paddock Condition"."Land System" = "{{3}}"."Land System"
and "Paddock Condition"."Watered" = "{{3}}"."Waterpoint Buffer Type"
"""




    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return Condition

    def __init__(self, layerName, paddock, paddockLayer, landSystemLayer, waterpointBufferLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = PaddockConditionLayer.QUERY.format(paddockId = paddock.id,
                                                               paddockName = paddock.name,
                                                               paddockStatus = paddock.status)

        super().__init__(layerName, query, PaddockConditionLayer.STYLE, paddockLayer, landSystemLayer, waterpointBufferLayer, conditionTable)



        

# with "Paddock Condition" as
# (with "Watered Areas" as
#     (select
#      st_union(geometry) as "geometry",
#      "Waterpoint Buffer Type",
#      "Status"
#      from "{2}"
#      group by "Waterpoint Buffer Type", "Status"),
#  "Paddock" as
# 	(select geometry from "Paddocks" where fid = 1)
# select
# st_intersection(st_intersection("Paddock".geometry, "{1}".geometry), "Watered Areas".geometry) as "geometry",
# "{1}".fid as "Land System",
# "{1}"."Name" as "Land System Name",
# "AE/km²" as "AE/km²",
# "Waterpoint Buffer Type",
# "Watered Areas"."Status" as "Watered Area Status"
# from "Paddock"
# inner join "{1}"
# on st_intersects("Paddock".geometry, "{1}".geometry)
# inner join "Watered Areas"
# on st_intersects("{1}".geometry, "Watered Areas".geometry))
# select
# "Paddock Condition".geometry,
# 1 as "Paddock",
# 'HOUSE HOLDING' as "Paddock Name",
# 'Built' as "Paddock Status",
# "Paddock Condition"."Land System",
# "Land System Name",
# "AE/km²",
# ifnull("{3}"."Condition", 'A') as "Condition",
# "Paddock Condition"."Waterpoint Buffer Type",
# "Watered Area Status"
# from
# "Paddock Condition" left outer join "{3}"
# on 1 = "{3}"."Paddock"
# and "Paddock Condition"."Land System" = "{3}"."Land System"
# and "Paddock Condition"."Waterpoint Buffer Type" = "{3}"."Waterpoint Buffer Type"



#     QUERY = """
# with "Paddock Condition" as
# (with "Watered Areas" as
#     (select
#      st_union(geometry) as "geometry",
#      "Waterpoint Buffer Type",
#      "Status"
#      from "{{1}}"
#      group by "Waterpoint Buffer Type", "Status")
# select
# st_intersection(st_intersection({paddockGeometry}, "{{0}}".geometry), "Watered Areas".geometry) as "geometry",
# "Land System",
# "Land System Name",
# "AE/km²" as "AE/km²",
# "Waterpoint Buffer Type",
# "Watered Areas"."Status" as "Watered Area Status"
# from "{{0}}"
# inner join "Watered Areas"
# on st_intersects("Watered Areas".geometry, st_intersection({paddockGeometry}, "{{0}}".geometry)))
# select
# "Paddock Condition".geometry,
# {paddockId} as "Paddock",
# '{paddockName}' as "Paddock Name",
# '{paddockStatus}' as "Paddock Status",
# "Paddock Condition"."Land System",
# "Land System Name",
# "AE/km²",
# ifnull("{{2}}"."Condition", 'A') as "Condition",
# "Paddock Condition"."Waterpoint Buffer Type",
# "Watered Area Status"
# from
# "Paddock Condition" left outer join "{{2}}"
# on {paddockId} = "{{2}}"."Paddock"
# and "Paddock Condition"."Land System" = "{{2}}"."Land System"
# and "Paddock Condition"."Waterpoint Buffer Type" = "{{2}}"."Waterpoint Buffer Type"

# """