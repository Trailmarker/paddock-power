# -*- coding: utf-8 -*-
from ..features.watered_area import WateredArea
from ..schemas.feature_status import FeatureStatus
from ..schemas.schemas import BUFFER_DISTANCE, FAR_BUFFER, FID, NEAR_BUFFER, STATUS, WATERPOINT, WATERPOINT_BUFFER_TYPE
from ..schemas.waterpoint_buffer_type import WaterpointBufferType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWateredAreaLayer(DerivedFeatureLayer):

    STYLE = "watered_area"

    QUERY = f"""
with
  "{WaterpointBufferType.Near.name}" as
	(select
	 st_union(geometry) as "geometry",
	 "{STATUS}"
	 from "{{1}}"
	 where "{WATERPOINT_BUFFER_TYPE}" = '{WaterpointBufferType.Near.name}'
	 group by "{STATUS}")
, "{WaterpointBufferType.Far.name}" as
	(select
	 st_union(geometry) as "geometry",
	 "{STATUS}"
	 from "{{1}}"
	 where "{WATERPOINT_BUFFER_TYPE}" = '{WaterpointBufferType.Far.name}'
	 group by "{STATUS}")
, "Farm" as
	(select st_union(geometry) as "geometry"
     from
	 (select geometry from "{{0}}"
	  union
	  select geometry from "{{1}}"))
select
	0 as "{FID}",
	st_collectionextract(geometry, 3),
	'{WaterpointBufferType.Near.name}' as "Watered",
	"{STATUS}"
from "{WaterpointBufferType.Near.name}"
union
select
	0 as "{FID}",
	st_collectionextract(st_difference("{WaterpointBufferType.Far.name}".geometry, "{WaterpointBufferType.Near.name}".geometry), 3),
	'{WaterpointBufferType.Far.name}' as "Watered",
	"{WaterpointBufferType.Far.name}"."{STATUS}"
from "{WaterpointBufferType.Far.name}"
inner join "{WaterpointBufferType.Near.name}"
on "{WaterpointBufferType.Far.name}"."{STATUS}" = "{WaterpointBufferType.Near.name}"."{STATUS}"
union
select
	0 as "{FID}",
	st_collectionextract(st_difference(st_difference("Farm".geometry, "{WaterpointBufferType.Far.name}".geometry), "{WaterpointBufferType.Near.name}".geometry), 3),
	'Unwatered' as "Watered",
	"{WaterpointBufferType.Far.name}"."{STATUS}"
from "Farm", "{WaterpointBufferType.Far.name}", "{WaterpointBufferType.Near.name}"
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WateredArea

    def __init__(self, layerName, paddockLayer, waterpointBufferLayer):
        super().__init__(layerName, DerivedWateredAreaLayer.QUERY, DerivedWateredAreaLayer.STYLE, paddockLayer, waterpointBufferLayer)
