# -*- coding: utf-8 -*-
from ..features.watered_area import WateredArea
from .derived_layer import DerivedLayer


class WateredAreaLayer(DerivedLayer):

    STYLE = "watered_area"

    QUERY = """
with
  "Near" as
	(select
	 st_union(geometry) as "geometry",
	 "Status"
	 from "{1}"
	 where "Waterpoint Buffer Type" = 'Near'
	 group by "Status")
, "Far" as
	(select
	 st_union(geometry) as "geometry",
	 "Status"
	 from "{1}"
	 where "Waterpoint Buffer Type" = 'Far'
	 group by "Status")
, "Farm" as
	(select st_union(geometry) as "geometry"
     from
	 (select geometry from "{0}"
	  union
	  select geometry from "{1}"))
select "geometry", 'Near' as "Watered", "Status"
from "Near"
union
select st_difference("Far".geometry, "Near".geometry), 'Far' as "Watered", "Far"."Status"
from "Far"
inner join "Near"
on "Far"."Status" = "Near"."Status"
union
select st_difference("Farm".geometry, "Far".geometry), 'Unwatered' as "Watered", "Far"."Status"
from "Farm", "Far"
"""

#     QUERY = """
# select st_union(geometry), "Waterpoint Buffer Type", "Status"
# from "{0}"
# group by "Waterpoint Buffer Type", "Status"

# """

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WateredArea

    def __init__(self, layerName, paddockLayer, waterpointBufferLayer):
        super().__init__(layerName, WateredAreaLayer.QUERY, WateredAreaLayer.STYLE, paddockLayer, waterpointBufferLayer)
