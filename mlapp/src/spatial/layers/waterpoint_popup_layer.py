# -*- coding: utf-8 -*-
from ..features.waterpoint_buffer import WaterpointBuffer
from .derived_layer import DerivedLayer


class WaterpointPopupLayer(DerivedLayer):

    STYLE = "waterpoint_popup"

    QUERY = """
with
  "Near" as
	(select
	 st_union(geometry) as "geometry", "Waterpoint", "Name", "Waterpoint Buffer Type", "Buffer Distance (m)", "Status" from "{{0}}"
	 where "Waterpoint Buffer Type" = 'Near'
	 and "Waterpoint" = {waterpointId}
	 group by "Status")
, "Far" as
	(select
	 st_union(geometry) as "geometry", "Waterpoint", "Name", "Waterpoint Buffer Type", "Buffer Distance (m)", "Status" from "{{0}}"
	 where "Waterpoint Buffer Type" = 'Far'
	 and "Waterpoint" = {waterpointId}
	 group by "Status")
select * 
from "Near"
union
select st_difference("Far".geometry, "Near".geometry), "Far"."Waterpoint", "Far"."Name", "Far"."Waterpoint Buffer Type", "Far"."Buffer Distance (m)", "Far"."Status"
from "Far"
inner join "Near"
on "Far"."Status" = "Near"."Status"
"""

# A version without the call to st_difference to eliminate the 'Near' buffer from the 'Far' buffer
#     SIMPLE_QUERY = """
# select * from "{{0}}"
# where "Waterpoint" = {waterpointId}
# and "Waterpoint Buffer Type" = 'Near'
# union
# select  from "{{0}}"
# """

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WaterpointBuffer

    def __init__(self, layerName, waterpoint, waterpointBufferLayer):
        # Burn in the Waterpoint specific parameters first …
        query = WaterpointPopupLayer.QUERY.format(waterpointId=waterpoint.id)

        super().__init__(layerName, query, WaterpointPopupLayer.STYLE, waterpointBufferLayer)
